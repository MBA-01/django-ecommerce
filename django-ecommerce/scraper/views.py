from django.shortcuts import render

# Create your views here.
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from .models import Domain, ScraperProduct
from .forms import DomainForm, ScraperProductForm
from shop.models import Product, Category
import subprocess
import os

def scrape_domain(request):
    if request.method == 'POST':
        form = DomainForm(request.POST)
        if form.is_valid():
            domain = form.save()
            run_scraping_script(domain.url)
            messages.success(request, "Scraping started.")
            return redirect('admin:scraper_domain_changelist')
    else:
        form = DomainForm()
    return render(request, '/scraper/scrape_domain.html', {'form': form})

def run_scraping_script(url):
    sanitized_url = url.replace('.', '_').replace('https://', '').replace('http://', '')
    script_path = os.path.join(os.path.dirname(__file__), '../main.py')
    subprocess.run(['python', script_path, url, sanitized_url])

def validate_product(request, pk):
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
    messages.success(request, f"Product '{official_product.name}' validated and added to official products.")
    return redirect('admin:scraper_scraperproduct_changelist')

def modify_product(request, pk):
    product = get_object_or_404(ScraperProduct, pk=pk)
    if request.method == 'POST':
        form = ScraperProductForm(request.POST, instance=product)
        if form.is_valid():
            form.save()
            messages.success(request, f"Product '{product.title}' modified.")
            return redirect('admin:scraper_scraperproduct_changelist')
    else:
        form = ScraperProductForm(instance=product)
    return render(request, 'scraper/scraperproduct_modify.html', {'form': form, 'product': product})

def cancel_product(request, pk):
    product = get_object_or_404(ScraperProduct, pk=pk)
    product.delete()
    messages.success(request, f"Product '{product.title}' canceled and deleted.")
    return redirect('admin:scraper_scraperproduct_changelist')
