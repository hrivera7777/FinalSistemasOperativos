from django.core.files import File

f = open('/path/to/hello.world', 'w')
myfile = File(f)