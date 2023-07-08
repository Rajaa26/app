# Uploader

This is a simple file sharing app written in python.
The is the enclaved version of the file sharing app that allows users to upload and download files, but the files are encrypted and decrypted in the enclave.

## RUN

Just run the following command:

```sh
sudo docker-compose build
sudo docker-compose up
```

## Usage

1. access the app at http://localhost/docs it runs on port 80.
1. upload a file with help of the swagger UI. use endpoint `/api/upload`
   it will respond with a json object containing the file id.
   ```json
   {
     "id": "bd6ce1dd-2c9f-4ba3-806d-4aa36756ca2d",
     "expires": 1688855384
   }
   ```
   note that there is an option to upload the file with a password, but it does not encrypt the file with the password. the password is used to prevent unauthorized access to the file. it has nothing to do with the encryption of the file. this encryption is handled by gramine.
1. Now check the /data folder, that is a generated in the root directory of the project. You will see a file with the name of the id you got in the previous step.
1. Try to open it with any text editor, you will see that it is encrypted.
1. Now try to download the file with the help of the swagger UI. use endpoint `/api/download/{id}`. You will get a file with the name of the id you provided in the previous step.
