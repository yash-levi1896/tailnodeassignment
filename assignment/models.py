from mongoengine import Document,EmbeddedDocument, StringField, IntField, ListField, DateTimeField, EmbeddedDocumentField

class User(Document):
    title = StringField(required=True, max_length=50)
    firstName = StringField(required=True, max_length=100)
    lastName = StringField(required=True, max_length=100)
    picture = StringField(required=True, max_length=100)
    user_id = StringField(required=True, max_length=100)

    def __str__(self):
        return f"User(title={self.title}, firstName={self.firstName}, lastName={self.lastName}, picture={self.picture})"

class Owner(EmbeddedDocument):
    id = StringField(required=True, max_length=100)
    title = StringField(required=True, max_length=50)
    firstname = StringField(required=True, max_length=100)
    lastname = StringField(required=True, max_length=100)
    picture = StringField(required=True, max_length=100)

    def __str__(self):
        return f"Owner(id={self.id}, title={self.title}, firstname={self.firstname}, lastname={self.lastname}, picture={self.picture})"

class Post(Document):
    image = StringField(required=True, max_length=1000)
    likes = IntField()
    tags = ListField(StringField())
    text = StringField()
    publishDate = DateTimeField()
    owner = EmbeddedDocumentField(Owner, required=True)

    def __str__(self):
        return f"Post(text={self.text})"
    

class Book(Document):
    image = StringField(required=True, max_length=1000)
    title=StringField(required=True,max_length=800)
    price=StringField(required=True,max_length=20)
    rating=StringField(required=True,max_length=20)
    availability=StringField(required=True,max_length=30)

    def __str__(self):
        return f"Book(name={self.title})"
    
