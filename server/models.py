from tortoise import fields, models

class User(models.Model):
    id = fields.IntField(pk=True)
    username = fields.CharField(max_length=50, unique=True)
    email = fields.CharField(max_length=100, unique=True)
    created_at = fields.DatetimeField(auto_now_add=True)

    def __str__(self):
        return self.username

class Story(models.Model):
    id = fields.IntField(pk=True)
    user = fields.ForeignKeyField('models.User', related_name='stories', null=True)
    prompt = fields.TextField()
    content = fields.TextField()
    generated_at = fields.DatetimeField(auto_now_add=True)

    def __str__(self):
        return f"Story {self.id} for {self.user}"

class VocabularySet(models.Model):
    id = fields.IntField(pk=True)
    user = fields.ForeignKeyField('models.User', related_name='vocab_sets', null=True)
    # Here, you could store words as a JSON string or comma-separated values
    words = fields.TextField()
    created_at = fields.DatetimeField(auto_now_add=True)

    def __str__(self):
        return f"VocabSet {self.id} for {self.user}"
