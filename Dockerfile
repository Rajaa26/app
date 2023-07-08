# original-src: gramineproject/gramine
# Gramine OS wrapper
# It creates an env SGX_SIGNER_KEY pointing to the key file  "/gramine-os/sgx-signer-key/enclaive-key.pem"
# It generates the private key and writes it to the file $SGX_SIGNER_KEY
FROM enclaive/gramine-os:jammy-33576d39
RUN apt-get update
# RUN apt-get install -y python3 
RUN apt-get install -y pip
RUN rm -rf /var/lib/apt/lists/*


ARG app_root_dir=./uploader
ARG WorkingDir=/app
ARG MANIFEST_FILE=uploader.manifest.toml
ARG MANIFEST_FILE_ARCH=app.manifest
ARG SIG_FILE=python3.sig
ARG App_Path_Specified=python3.manifest.sgx
# Bins.
# FastAPI
WORKDIR ${WorkingDir}
COPY ./${MANIFEST_FILE} ./${MANIFEST_FILE}

VOLUME /data/

# Gramine manifest preprocessor
RUN gramine-manifest -Darch_libdir=/lib/x86_64-linux-gnu $MANIFEST_FILE $MANIFEST_FILE_ARCH

RUN gramine-sgx-sign \
    --key "$SGX_SIGNER_KEY" \
    --manifest $MANIFEST_FILE_ARCH \ 
    --output $App_Path_Specified \ 
    -s $SIG_FILE

RUN gramine-sgx-get-token --sig $SIG_FILE --output python3.token
COPY $app_root_dir ${WorkingDir}/uploader
WORKDIR ${WorkingDir}/uploader

# Update requirements.txt and install dependencies

RUN python3 -m pip install -r requirements.txt

WORKDIR ${WorkingDir}



RUN gramine-argv-serializer "python3" "-m" "uvicorn" "app.uploader:app" "--host" "0.0.0.0" "--port" "80" > args.txt
ENTRYPOINT ["/usr/local/bin/gramine-sgx","python3"] 