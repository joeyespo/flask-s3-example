Flask S3 Example
================

Just a quick example on how to run S3 in Flask.
This example uses Flask config variables, allowing you to run out-of-the-box.


Usage
-----

1. Copy `config.py.example` to `config.py`
2. Set your AWS config variables
3. Run `flask_s3_example.py`


Setting Up AWS
--------------

Be sure to set your permissions from the AWS management console. To
run from localhost, use this:

```html
<?xml version="1.0" encoding="UTF-8"?>
<CORSConfiguration xmlns="http://s3.amazonaws.com/doc/2006-03-01/">
    <CORSRule>
        <AllowedOrigin>*</AllowedOrigin>
        <AllowedMethod>GET</AllowedMethod>
        <AllowedMethod>POST</AllowedMethod>
        <AllowedMethod>PUT</AllowedMethod>
        <AllowedMethod>DELETE</AllowedMethod>
        <AllowedHeader>*</AllowedHeader>
    </CORSRule>
</CORSConfiguration>
```

Note that you should change `<AllowedOrigin>*</AllowedOrigin>` to
`<AllowedOrigin>http://*.example.com</AllowedOrigin>` when you're done tinkering.
