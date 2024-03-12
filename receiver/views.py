from django.shortcuts import render, redirect
from admin_mod.models import User
from provider.models import post, toysDes, groceryDes, clothDes, foodDes, otherDes,FeedbackTab
from receiver.models import Order
from django.contrib import messages
from datetime import datetime
from admin_mod import views
from django.urls import reverse
from django.http import JsonResponse
from django.http import HttpResponse




def check_user_login_status(request):
   try:
    user_id=request.session['user_id']
   except KeyError:
    #clear previous error messages
      
    messages.error(request,"Please login before acessing the page")
    return redirect('/login')
def is_receiver(request):
  user_id=request.session['user_id']
  user_role=User.objects.get(id=user_id).role
  return user_role=='receiver'  

def give_all_posts():
  #send all the posts as list of dictionaries 
  combined_posts = []
  #filter live(which are not ordered) posts
  posts=post.objects.filter(status='live')
  #add each user_post (along with category details) to combined_posts
  for user_post in posts:
    post_data={
      'item_name':user_post.name,
      'image':user_post.photo.url,
      'location':user_post.location,
      'drop_pickup':user_post.drop_pickup
    }
    #take details of the user who made the user_post
    user_details=User.objects.get(id=user_post.user_id)
    post_data['user_name']=user_details.username
    post_data['post_id']=user_post.id
    post_data['category']=user_post.category
    category=user_post.category
    if category=='food':
      description=foodDes.objects.get(id=user_post.description_id)
      post_data['quantity']=user_post.quantity
      post_data['expiry_date']=description.expiry_date.strftime('%Y-%m-%d')
      post_data['expiry_time']=description.expiry_time.strftime('%H:%M')
    combined_posts.append(post_data) 
  data={'posts':combined_posts}
  return data

def home(request):
   #check wether the user is logged in or not
   try:
    user_id=request.session['user_id']
   except KeyError:
    #clear previous error messages
      
    messages.error(request,"Please login before acessing the page")
    return redirect('/login')
  #if the user is not receiver redirect to login
   if(not is_receiver(request)):
    #clear previous error messages
      
    messages.error(request,"Sorry,you dont have permission")
    return redirect('/login')
   #take all posts into 'data' dictionary
   data=give_all_posts()
   return render(request, "receiver/dashboard.html", {'data':data}) 

  

def view_post(request,post_id):
  #check if user is logged in or not
  try:
    user_id=request.session['user_id']
  except KeyError:
    #clear previous error messages
      
    messages.error(request,"Please login before acessing the page")
    return redirect('/login') 
  #check wether the user_post id is valid
  
  try:
      user_post = post.objects.get(id=post_id)
      post_data={
      'item_name':user_post.name,
      'image':user_post.photo.url,
      'location':user_post.location,
      'drop_pickup':user_post.drop_pickup
    }
    #take details of the user who made the user_post
      user_details=User.objects.get(id=user_post.user_id)
      post_data['user_name']=user_details.username
      post_data['post_id']=user_post.id
      post_data['category']=user_post.category
    #add the description data based on the category
      if user_post.category=='food':
        description=foodDes.objects.get(id=user_post.description_id)
        post_data['description'] = {
        'desc': description.desc,
        'expiry_date': description.expiry_date.strftime('%Y-%m-%d'),
        'expiry_time': description.expiry_time.strftime('%H:%M'),
        }
       
      elif user_post.category=='toys':
        description=toysDes.objects.get(id=user_post.description_id)
        post_data['description'] = {
            'age_group': description.age_group,
            'condition': description.condition,
            'desc': description.desc
        }
      elif user_post.category=='clothes':
        description=clothDes.objects.get(id=user_post.description_id)
        post_data['description'] = {
            'gender': description.gender,
            'condition': description.condition,
            'size': description.size,
            'desc': description.desc
        }
      elif user_post.category=='others':
        description=otherDes.objects.get(id=user_post.description_id)
        post_data['description'] = {
            'desc': description.desc
        }
      elif user_post.category=='groceries':
        description=groceryDes.objects.get(id=user_post.description_id)
        post_data['description'] = {
            'desc': description.desc,
            'expiry_date': description.expiry_date.strftime('%Y-%m-%d'),
            'expiry_time': description.expiry_time.strftime('%H:%M')
        }
      post_data['quantity'] = user_post.quantity
      return render(request, 'receiver/viewPost.html',{'post_data':post_data})
  except post.DoesNotExist:
        #clear previous error messages
          
        messages.error(request, 'Sorry, the user_post does not exist')
        return redirect('/receiver/home')
        

def order(request):
    print('gotcha')
    check_user_login_status(request)
    #take post_id from the submitted form
    post_id = request.POST.get('post_id')
    print(post_id)
    try:
     ordered_post=post.objects.get(id=post_id)
     provider_location=ordered_post.location
     receiver_user_id=request.session['user_id']
     receiver_user=User.objects.get(id=receiver_user_id)
     delivery_location=User.objects.get(id=receiver_user_id).location
     #take quantity from the submitted form
     quantity=request.POST.get('quantity')
     
     #create a new order in order table
     new_order=Order.objects.create(
       ordered_post=ordered_post, receiver_user=receiver_user,receiver_location=delivery_location,
       quantity=quantity
       )
     data = {
       'image':ordered_post.photo.url,
     }
     data['message']='Order successful'
     data['location']=provider_location
   
     #render order tracking page with sucess message
     return HttpResponse(status=204)  # Return a 204 No Content response
      
    #if there is no such user_post
    except post.DoesNotExist:   
      #clear previous error messages
        
      #render the page with the specific error(not implemented)
      messages.error(request, 'Sorry there is no such item or the item is already ordered')
      return redirect('/receiver/home')
    
def track_order(request,post_id):
    try:
     user_id=request.session['user_id']
    except KeyError:
    #clear previous error messages
     messages.error(request,"Please login before acessing the page")
     return redirect('/login')
    #user can only track his active order(not yet implemeted)
    try:
     receiver_location=User.objects.get(id=user_id).location
     ordered_post=post.objects.get(id=post_id)
     provider_location=ordered_post.location

     data = {
       'image':ordered_post.photo.url,
     }
     data['message']='Order successful'
     data['provider_location']=provider_location
     data['receiver_location']=receiver_location
     data['post_id']=post_id    
   
     #render order tracking page with sucess message
     return render(request,"receiver/trackOrder.html",{'data':data})
    
     
    #if there is no such user_post
    except post.DoesNotExist:   
      #clear previous error messages
        
      messages.error(request, 'Sorry there is no such item or the item is already ordered')
      return redirect('/receiver/home')


def waiting_page(request):
  check_user_login_status(request)
  return render(request,'receiver/waitingPage.html')
    

#all orders of the user
def order_history(request):
   #get the user id
   user_id=request.session['user_id']
   #all orders made by user
   orders=Order.objects.filter(receiver_user_id=user_id)
   #seperate all kinds of orders made by this user
   accepted=[]
   pending=[]
   rejected=[]
   delivered=[] #receiver have a button wether the order is delivered or not when he clicks on that the status will be updated to delivered(not yet implemented)  
   for order in orders:
       order_details={}
       order_details['status']=order.status
       order_details['order_id']=order.id
       order_details['date']=order.date_time.strftime('%d-%m-%Y')
       order_details['time']=order.date_time.strftime('%H:%M')
       order_details['quantity']=order.quantity

       if(order.status=='accepted'):
         accepted.append(order_details)
       elif(order.status=='pending'):
         pending.append(order_details) #here
       elif(order.status=='rejected'):
         rejected.append(order_details)
       else:
         delivered.append(order_details)
       
     #take image,item_name,user_post location from user_post table
       user_post=post.objects.get(id=order.ordered_post_id)
       order_details['image']=user_post.photo.url
       order_details['item_name']=user_post.name
       order_details['location']=user_post.location
       order_details['post_id']=order.ordered_post_id
     #take location from user table
      
   all_orders={
      'accepted':accepted,
      'pending':pending,
      'rejected':rejected,
      'delivered':delivered,
    }
   return render(request,'receiver/orderHistory.html',{'orders':all_orders})
           
def feedback(request,post_id):
  data={'post_id':post_id}
  return render(request,'receiver/feedback.html',{'data':data})

def send_feedback(request):
   if request.method == 'POST':
    # Extract data from the form
    rating = request.POST.get('star')
    feedback_text = request.POST.get('feedback')
    post_id=request.POST.get('post_id')
    user_id=request.session.get('user_id')
    
    user_post=post.objects.get(id=post_id)
    user=User.objects.get(id=user_id)
    #create a new feedback
    feedback = FeedbackTab.objects.create(
            post_id=user_post,
            given_by=user,
            rating=rating,
            feedback=feedback_text
        )
    print("success")
    return HttpResponse(status=204)
  #  else:
  #   data=give_all_posts()
  #   messages.error(request, "Can't access")
  #   return redirect('/receiver/home')
  
  
     
     
     
  
     
