from django.shortcuts import render, redirect
from admin_mod.models import User
from provider.models import Post, toysDes, groceryDes, clothDes, foodDes, otherDes
from receiver.models import Order
from django.contrib import messages
from datetime import datetime

def give_all_posts():
  #send all the posts as list of dictionaries 
  combined_posts = []
  #filter live(which are not ordered) posts
  posts=Post.objects.filter(status='live')
  #add each post (along with category details) to combined data
  for post in posts:
    post_data={
      'item_name':post.name,
      'image':post.photo.url,
      'location':post.location,
      'drop_pickup':post.drop_pickup
    }
    #take details of the user who made the post
    user_details=User.objects.get(id=post.user_id)
    post_data['user_name']=user_details.username
    post_data['post_id']=post.id
    category=post.category
    if category=='food':
      description=foodDes.objects.get(id=post.description_id)
      post_data['quantity']=post.quantity
      post_data['expiry_date']=description.expiry_date
      post_data['expiry_time']=description.expiry_time
    
    combined_posts.append(post_data) 
  data={'posts':combined_posts}
  return data

def dashboard(request):
  data=give_all_posts()
  print(data)
  return render(request, "receiver/dashboard.html", {'data':data})  

def view_post(request,post_id):
   try:
      post = Post.objects.get(id=post_id)
        
      post_data={
      'item_name':post.name,
      'image':post.photo.url,
      'location':post.location,
      'drop_pickup':post.drop_pickup
    }
    #take details of the user who made the post
      user_details=User.objects.get(id=post.user_id)
      post_data['user_name']=user_details.username
      post_data['post_id']=post.id
      category=post.category
      if category=='food':
        description=foodDes.objects.get(id=post.description_id)
        post_data['quantity']=post.quantity
        post_data['expiry_date']=description.expiry_date
        post_data['expiry_time']=description.expiry_time
        return render(request, "receiver/viewPost.html",{'post_data':post_data})
   except Post.DoesNotExist:
        messages.error(request, 'Sorry, the post does not exist.')
        return redirect('/receiver')
    
        

def order(request,post_id):
    #not fully completed 
    try:
     ordered_post=Post.objects.get(id=post_id)
     #take the user id of receiver(have to make it dynamic)
     receiver_user_id=1
     receiver_user=User.objects.get(id=receiver_user_id)
     delivery_location=User.objects.get(id=receiver_user_id).location
     quantity=20#it should be (request.POST.quantity)
     #create a new order in order table
     new_order=Order.objects.create(
       ordered_post=ordered_post, receiver_user=receiver_user,receiver_location=delivery_location,
       quantity=quantity
       )
     data = {
       'image':ordered_post.photo.url,
     }
     data['message']='Order successful'
     
     #render order tracking page with sucess message
     return render(request,"receiver/trackOrder.html",{'data':data})
    
     
    #if there is no such post
    except Post.DoesNotExist:   
      #render the page with the specific error(not implemented)
      messages.error(request, 'Sorry there is no such item or the item is already ordered')
      return redirect('/receiver')
     
