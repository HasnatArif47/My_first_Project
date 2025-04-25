from django.db import migrations

def create_superuser_with_permissions(apps, schema_editor):
    User = apps.get_model('auth', 'User')
    Group = apps.get_model('auth', 'Group')
    Permission = apps.get_model('auth', 'Permission')

    # Create superuser if not exists
    if not User.objects.filter(username='customadmin').exists():
        user = User.objects.create_superuser(
            username='customadmin',
            email='customadmin@example.com',
            password='securepassword123'
        )

        # Example: Give this superuser specific permissions
        # Get some permissions by codename
        perm1 = Permission.objects.get(codename='add_user')
        perm2 = Permission.objects.get(codename='change_user')
        perm3 = Permission.objects.get(codename='delete_user')

        # Assign permissions directly to the user
        user.user_permissions.add(perm1, perm2, perm3)

        # You could also add the user to a group here, if needed
        # group = Group.objects.get(name='Editors')
        # user.groups.add(group)

        user.save()

def remove_superuser(apps, schema_editor):
    User = apps.get_model('auth', 'User')
    User.objects.filter(username='customadmin').delete()

class Migration(migrations.Migration):

    dependencies = [
        ('home', '0001_initial'),
    ]

    operations = [
        migrations.RunPython(create_superuser_with_permissions, reverse_code=remove_superuser),
    ]
