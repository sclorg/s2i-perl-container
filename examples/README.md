# S2I Sample Applications for Perl Builder Image

This is a very basic sample application repository that can be built and deployed
on [OpenShift](https://www.openshift.com) using the [Perl builder image](https://github.com/sclorg/s2i-perl-container).

The application serves a single static html page via perl, while also installing Math::Round package from cpan.

To build and run the application:

```
$ s2i build --context-dir=examples/sample-test-app https://github.com/sclorg/s2i-perl-container centos/perl-524-centos7 myperlimage
$ docker run -p 8080:8080 myperlimage
$ # browse to http://localhost:8080
```

You can also build and deploy the application on OpenShift, assuming you have a
working `oc` command line environment connected to your cluster already:

`$ oc new-app --context-dir=examples/sample-test-app centos/perl-524-centos7~https://github.com/sclorg/s2i-perl-container`

You can also deploy the sample template for the application:

`$ oc new-app -f https://raw.githubusercontent.com/sclorg/s2i-perl-container/master/examples/templates/sample-test-app.json`

