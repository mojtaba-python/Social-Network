from django.contrib.auth.models  import BaseUserManager


class UserManager(BaseUserManager):
    def create_user(self, phone_number, email, full_name, password, bio, image):
        if not phone_number:
            raise ValueError('user must have phone number')
        if not email:
            raise ValueError('user must have email')
        if not full_name:
            raise ValueError('user must have full name')

        user = self.model(phone_number=phone_number, email=self.normalize_email(email), full_name=full_name, bio=bio, image=image)
        user.set_password(password)
        user.save(using=self._db)
        return user


    def create_superuser(self, phone_number, email, full_name, password, bio):
        user = self.create_user(phone_number, email, full_name, password, bio=bio)
        user.is_admin = True
        user.save(using=self._db)
        return user
        