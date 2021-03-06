from django.shortcuts import render, redirect, get_object_or_404
from ..forms.tradeForm import SubmitForm
from datastore.models.product import Product
from datastore.models.prodsub import ProductSubmit
import datetime
from authentication.decorators import customer_required
from convertdate import persian

@customer_required
def submitProduct(request):
    # add active/deactive
    if request.method == 'POST':
        form = SubmitForm(request.POST)
        if form.is_valid():
            subprod = form.instance
            subprod.quantity = request.POST['quantity']
            subprod.submitter = request.user.unprivilegeduser.customer
            today = datetime.date.today()
            subprod.date = today
            subprod.active = True
            subprod.save()
            return redirect('reporting:prod_list')

    else:
        form = SubmitForm()

    return render(request, 'tradeproduct/submitProduct.html', {'form':form})

@customer_required
def submit_details(request, prodsub_id):
    subprod = get_object_or_404(ProductSubmit, pk=prodsub_id)
    prod_tarikh = subprod.date
    tarikh = persian.from_gregorian(prod_tarikh.year, prod_tarikh.month, prod_tarikh.day)
    return render(request, 'tradeproduct/submittedProduct_details.html', {'submittedProduct': (subprod, tarikh), 'activated': subprod.active})

@customer_required
def delete_submittedProduct(request, delete_id):
    if request.method == "POST":
        ps = get_object_or_404(ProductSubmit, pk=delete_id)
        ps.delete()
        # send a message that it was successfully deleted

    return redirect('reporting:prod_list')

@customer_required
def change_details(request, change_id):
    if request.method == "POST":
        form = SubmitForm(request.POST)
        subprod = ProductSubmit.objects.get(pk=change_id)
        if form.data['quantity'] == '0':
            subprod.delete()
        else:
            subprod.quantity = form.data['quantity']
            subprod.location = form.data['location']
            subprod.price = form.data['price']
            today = datetime.date.today()
            subprod.date = today
            subprod.save()

        return redirect('reporting:prod_list')

    else:
        subprod = get_object_or_404(ProductSubmit, pk=change_id)
        form = SubmitForm(instance=subprod)
        form.fields['product'].widget.attrs['disabled'] = 'disabled'
        form.fields['province'].widget.attrs['disabled'] = 'disabled'
        return render(request, 'tradeproduct/change_details.html', {'form': form, 'subp_id': change_id,
                                                                    'activated': subprod.active, 'meghdar': subprod.quantity})
