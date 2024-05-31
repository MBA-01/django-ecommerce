from django.contrib import admin
from .models import Domain, ScraperProduct
from shop.models import Category,Product
from .forms import DomainForm, ScraperProductForm
from django.urls import path, reverse
from django.shortcuts import redirect, render, get_object_or_404
from django.utils.html import format_html
from author.models import AuthorProfile
import subprocess
import os
import logging
import json
from django_ecommerce.settings import BASE_DIR

@admin.register(Domain)
class DomainAdmin(admin.ModelAdmin):
    list_display = ('name', 'url')
    form = DomainForm
    change_list_template = 'admin/scraper/domain_changelist.html'
    actions = ['start_scraping','import_domain']
    

    def get_urls(self):
        urls = super().get_urls()
        custom_urls = [
            path('scrape/', self.admin_site.admin_view(self.scrape_domain), name='scraper_domain_scrape'),
            # path('import/', self.admin_site.admin_view(self.import_products), name='scraper_import_products'),
            path('import/<int:pk>/', self.admin_site.admin_view(self.import_domain), name='scraper_import_domain'),

        ]
        return custom_urls + urls

    def scrape_domain(self, request):
        if request.method == 'POST':
            form = DomainForm(request.POST)
            if form.is_valid():
                domain = form.save()
                # Trigger the scraping logic here
                self.run_scraping_script(domain.url)
                self.message_user(request, "Scraping started.")
                #return redirect('admin:scraper_domain_changelist')
                return redirect('..')
        else:
            form = DomainForm()
        return render(request, 'admin/scraper/scrape_domain.html', {'form': form})

    def start_scraping(self, request, queryset):
        for domain in queryset:
            self.run_scraping_script(domain.url)
        self.message_user(request, "Scraping started for selected domains.")

    start_scraping.short_description = "Start scraping for selected domains"

    def run_scraping_script(self, url):
        sanitized_url = url.replace('.', '_').replace('https://', '').replace('http://', '')
        script_path = os.path.join(os.path.dirname(__file__), './Product_scraper/main.py')
        result = subprocess.run(['python', script_path, url, sanitized_url],capture_output=True, text=True)
        logging.info(result.stdout)
        logging.error(result.stderr)
        #self.message_user(self.request, f"Scraping result: {result.stdout}\nErrors: {result.stderr}")


    def import_domain(self, request, pk):
        domain = get_object_or_404(Domain, pk=pk)
        self.run_import(domain.url)
        self.message_user(request, f"Import started for {domain.name}.")
        return redirect('..')

    def start_importing(self, request, queryset):
        for domain in queryset:
            self.run_import(domain.url)
        self.message_user(request, "Import started for selected domains.")

    start_importing.short_description = "Start importing for selected domains"

    def run_import(self, url):
        sanitized_url = url.replace('.', '_').replace('https://', '').replace('http://', '')
        json_path = os.path.join(BASE_DIR, f'scraper/Product_scraper/data/{sanitized_url}_product_info_details.json')
        
        try:
            with open(json_path, 'r') as json_file:
                products = json.load(json_file)

            for product_data in products:
                category, created = Category.objects.get_or_create(name=sanitized_url)
                official_product = Product.objects.create(
                    name=product_data['title'],
                    photo=product_data['images'][0],  # Assuming you'll handle photo URL to ImageField conversion
                    price=int(product_data['price'].replace('£', '').replace('$', '').replace('€', '')),  # Adjust based on your price format
                    details=product_data['description'],
                    category=category,
                    author=AuthorProfile.objects.first(),  # Assuming the first AuthorProfile for simplicity
                    is_draft=False,
                    inventory=1
                )
        except FileNotFoundError:
            logging.error(f"No JSON file found for domain {sanitized_url}")
    
    # def import_button(self, obj):
    #     return format_html('<a class="button" href="{}">Import Products</a>', reverse('admin:scraper_import_products'), args=[obj.pk])
    # import_button.short_description = 'Import Products'
    # import_button.allow_tags = True

    # def import_products(self, request, pk):
    #     #if request.method == 'POST':
    #     #domain_name = request.POST.get('domain')
    #     domain = get_object_or_404(Domain, pk=pk)

    #     json_path = os.path.join(BASE_DIR, f'scraper/Product_scraper/data/{domain.name.replace(" ", "_").lower()}_product_info_details.json')
            
    #     try:
    #         with open(json_path, 'r') as json_file:
    #             products = json.load(json_file)

    #         for product_data in products:
    #             category, created = Category.objects.get_or_create(name=domain.name)
    #             official_product = Product.objects.create(
    #                 name=product_data['title'],
    #                 photo=product_data['images'][0],  # Assuming you'll handle photo URL to ImageField conversion
    #                 price=int(product_data['price'].replace('£', '').replace('$', '').replace('€', '')),  # Adjust based on your price format
    #                 details=product_data['description'],
    #                 category=category,
    #                 author=request.user.authorprofile,  # Assuming the admin user has an AuthorProfile
    #                 is_draft=False,
    #                 inventory=1
    #             )
    #         self.message_user(request, f"Products imported successfully from {domain.name}")
    #     except FileNotFoundError:
    #         self.message_user(request, f"No JSON file found for domain {domain.name}", level=logging.ERROR)
    #     return redirect('admin:scraper_import_products')
    # import_products.short_description = "Import products for selected domain"

        #return render(request, 'admin/scraper/import_products.html', {'domains': Domain.objects.all()})

@admin.register(ScraperProduct)
class ScraperProductAdmin(admin.ModelAdmin):
    list_display = ('title', 'domain', 'price', 'link', 'validate_button', 'modify_button', 'cancel_button')
    form = ScraperProductForm
    
    # new 
    


    def get_urls(self):
        urls = super().get_urls()
        custom_urls = [
            path('validate/<int:pk>/', self.admin_site.admin_view(self.validate_product), name='scraper_scraperproduct_validate'),
            path('modify/<int:pk>/', self.admin_site.admin_view(self.modify_product), name='scraper_scraperproduct_modify'),
            path('cancel/<int:pk>/', self.admin_site.admin_view(self.cancel_product), name='scraper_scraperproduct_cancel'),
            #path('import/', self.admin_site.admin_view(self.import_products), name='scraper_import_products'),

        ]
        return custom_urls + urls

    def validate_product(self, request, pk):
        product = get_object_or_404(ScraperProduct, pk=pk)
        category, created = Category.objects.get_or_create(name=product.domain.name)
        official_product = Product.objects.create(
            name=product.title,
            photo=product.images[0],  # Assuming you'll handle photo URL to ImageField conversion
            price=int(product.price.strip('$')),  # Assuming the price is formatted as a string with a currency symbol
            details=product.description,
            category=category,
            author=request.user.authorprofile,  # Assuming the admin user has an AuthorProfile
            is_draft=False,
            inventory=1
        )
        product.delete()
        self.message_user(request, f"Product '{official_product.name}' validated and added to official products.")
        return redirect('admin:scraper_scraperproduct_changelist')

    def modify_product(self, request, pk):
        product = get_object_or_404(ScraperProduct, pk=pk)
        if request.method == 'POST':
            form = ScraperProductForm(request.POST, instance=product)
            if form.is_valid():
                form.save()
                self.message_user(request, f"Product '{product.title}' modified.")
                return redirect('admin:scraper_scraperproduct_changelist')
        else:
            form = ScraperProductForm(instance=product)
        return render(request, 'admin/scraper/scraperproduct_modify.html', {'form': form, 'product': product})

    def cancel_product(self, request, pk):
        product = get_object_or_404(ScraperProduct, pk=pk)
        product.delete()
        self.message_user(request, f"Product '{product.title}' canceled and deleted.")
        return redirect('admin:scraper_scraperproduct_changelist')

    def validate_button(self, obj):
        return format_html('<a class="button" href="{}">Validate</a>', reverse('admin:scraper_scraperproduct_validate', args=[obj.pk]))
    validate_button.short_description = 'Validate'
    validate_button.allow_tags = True

    def modify_button(self, obj):
        return format_html('<a class="button" href="{}">Modify</a>', reverse('admin:scraper_scraperproduct_modify', args=[obj.pk]))
    modify_button.short_description = 'Modify'
    modify_button.allow_tags = True

    def cancel_button(self, obj):
        return format_html('<a class="button" href="{}">Cancel</a>', reverse('admin:scraper_scraperproduct_cancel', args=[obj.pk]))
    cancel_button.short_description = 'Cancel'
    cancel_button.allow_tags = True

    # def import_button(self, obj):
    #     return format_html('<a class="button" href="{}">Import Products</a>', reverse('admin:scraper_import_products'))
    # import_button.short_description = 'Import Products'
    # import_button.allow_tags = True

    # def import_products(self, request):
    #     if request.method == 'POST':
    #         domain_name = request.POST.get('domain')
    #         json_path = os.path.join(BASE_DIR, f'scraper/Product_scraper/data/{domain_name}_product_info_details.json')
            
    #         try:
    #             with open(json_path, 'r') as json_file:
    #                 products = json.load(json_file)

    #             for product_data in products:
    #                 category, created = Category.objects.get_or_create(name=domain_name)
    #                 official_product = Product.objects.create(
    #                     name=product_data['title'],
    #                     photo=product_data['images'][0],  # Assuming you'll handle photo URL to ImageField conversion
    #                     price=int(product_data['price'].replace('£', '').replace('$', '').replace('€', '')),  # Adjust based on your price format
    #                     details=product_data['description'],
    #                     category=category,
    #                     author=request.user.authorprofile,  # Assuming the admin user has an AuthorProfile
    #                     is_draft=False,
    #                     inventory=1
    #                 )
    #             self.message_user(request, f"Products imported successfully from {domain_name}")
    #         except FileNotFoundError:
    #             self.message_user(request, f"No JSON file found for domain {domain_name}", level=logging.ERROR)
    #         return redirect('admin:scraper_scraperproduct_changelist')
        
    #     return render(request, 'admin/scraper/import_products.html', {'domains': Domain.objects.all()})