from BlogApp.models import users,posts

#authenticate
#username
#password

# username="anu"
# password="Password@123"
#user={"id":1,"username":"akhil","email":"akhil@gmail.com","password":"password@123"}

# user=[user for user in users if user["username"]==username and user["password"]==password]
# print(user)

session={}
def signin_required(fn):  #all time signin(login)
    def wrapper(*args,**kwargs):    #for giving many parameters
        if("user") in session:
            return fn(*args,**kwargs)
        else:
            print("u must login")
    return wrapper


def authenticate(**kwargs):
    username=kwargs.get("username")
    password=kwargs.get("password")
    user = [user for user in users if user["username"] == username and user["password"] == password]
    return user

#print(authenticate(username="anu",password="Password@123"))



class SignInView:


    def post(self,*args,**kwargs):
        username=kwargs.get("username")
        password=kwargs.get("password")
        user=(authenticate(username=username,password=password))
        if user:
            session["user"]=user[0]
            print("success")
        else:
            print("invalid")

class PostsView():        #1 post create
    @signin_required
    def get(self,*args,**kwargs):

        return posts

    @signin_required
    def post(self,*args,**kwargs):

        #print(kwargs)
        userId=session["user"]["id"]
        kwargs["userId"]=userId
        posts.append(kwargs)
        print(posts)
class MyPostListView:

    @signin_required
    def get(self,*args,**kwargs):
        print(session)
        userId=session["user"]["id"]
        print(userId)
        my_posts=[posts for post in posts if post["userId"]==userId]
        return my_posts

class PostsDetailsView:                   #1 specific post call



    def get_object(self,id):
        post=[post for post in posts if post["postId"]==id]
        return post

    @signin_required
    def get(self,*args,**kwargs):
        post_id=kwargs.get("post_id")
        post=self.get_object(post_id)
        return post

    @signin_required                                               #decorators==>for functionaloities,authentication,not for attributes
    def delete(self,*args,**kwargs):
        post_id=kwargs.get("post_id")
        data=self.get_object(post_id)
        #data=[post for post in posts if post["postId"]==post_id]
        if data:
            post=data[0]
            posts.remove(post)
            print("post removed")
            print(len(posts))

    @signin_required
    def put(self,*args,**kwargs):        #for update
        print(kwargs)
        post_id=kwargs.get("post_id")
        instance=self.get_object(post_id)
        data=kwargs.get("data")               #updating data
        if instance:
            post_obj=instance[0]
            post_obj.update(data)
            return post_obj

class LikeView:

    @signin_required
    def get(self,*args,**kwargs):
        postid=kwargs.get("postid")
        post=[post for post in posts if post["postId"]==postid]
        if post:
            post=post[0]
            userid=session["user"]["id"]
            post["liked_by"].append(userid)
            print(post)


def signout(*args,**kwargs):
    user=session.pop("user")
    print("the",user["username"],"has been logged out")
    # print(f"the user {user['username']} has been logged out")

log=SignInView()
log.post(username="richard",password="Password@123")

like=LikeView()
like.get(postid=6)

signout()

# myposts=MyPostListView()
# print(myposts.get())
# post_detail=PostDetailsView()
# post_detail.delete(post_id=6)            #for all remove post(7),ge==1 post delete
# print(post_detail.get(post_id=6))
# print(post_detail.get(post_id=5))

# data={
#     "title":"newtitle"
# }
# postdetails=PostDetailsView()
# print(postdetails.put(post_id=4,data=data))   #post id=5,replace 4 to data

# print(session)
# data=PostsView()
# print(data.get())
# data.post(postId=9,
#           title="hello there",
#           content="hhhlll",
#           liked_by=[])
#
#now="ekm"
#name="ajay"
#frm"="tvm"
#hai all am ajay from tvm at present am in ekm
#print(hai all am",name,"frm,"at present am in",now)
#print(f"hai all am{name} from {frm} at present am in {now}")

#GET==>RETRIEVE,
#POST==>CREATE,
#PUT/PATCH==>EDIT,
#DELETE==>DELETE


