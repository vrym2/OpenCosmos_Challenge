# Google Cloud Platform (GCP)

__Note__: Information regarding Google cloud services.

* Install [Google Cloud SDK](https://cloud.google.com/sdk/docs/install)(click the link for instructions) on you machine, to utilise Google Cloud Services via CLI.

* Install [Google Cloud Storage](https://cloud.google.com/storage/docs/gsutil_install) on your machine, to use cloud storage commands via CLI.

* Create a new project on the platform or, set a project as default in you current machine.
```
$ gcloud projects create PROJECT_ID # To create a project
$ gcloud config set project PROJECT_ID # To set a project as default
```

__Warning__: Make sure to enable billing for your project, as the google demands billing when using their services.

* Enable Google cloud storage API.
```
$ gcloud services enable storage-api.googleapis.com # Google Cloud Storage JSON API    
$ gcloud services enable storage-component.googleapis.com # Cloud Storage
$ gcloud services enable storage.googleapis.com # Cloud Storage API
```

* Create a bucket in the cloud storage.
```
$ gcloud storage buckets create gs://BUCKET_NAME
```

* Look at the `IAM` policy of the current project by running the below command, if the role of `storage.admin`, `storage.objectAdmin` and `storage.objectCreator` is not given to the service account you are using, go to the [IAM](https://console.cloud.google.com/iam-admin/iam?authuser=1&project=kinetic-hydro) page of your project, and grant the access to the appropriate service account and to your email ID.
```
$ gcloud projects get-iam-policy PROJECT_ID
``` 

That's it, you are all set!