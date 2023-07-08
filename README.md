# Demo.

This is a simple file sharing app written in python.

## Different between this demo version of non-enclaved version and the enclaved version

The enclaved version is a file sharing app that allows users to upload and download files, but the files are encrypted and decrypted in the enclave.

## How to run the demo

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
1. Now check the /data folder, that is a generated in the root directory of the project. You will see a file with the name of the id you got in the previous step.
1. Try to open it with any text editor, you will see that it is readable, since it is not encrypted. But if you try to open it with the enclaved version of the app, you will see that it is not readable.
