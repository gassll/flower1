# from django.shortcuts import render, redirect
# from django.contrib.auth.decorators import login_required
# from .forms import OrderForm
#
# @login_required
# def create_order_view(request):
#     if request.method == 'POST':
#         form = OrderForm(request.POST)
#         if form.is_valid():
#             order = form.save(commit=False)
#             order.user = request.user
#             order.save()
#             return redirect('home')
#
#     else:
#         form = OrderForm()
#
#     return render(request,'',{'form':form})
#

