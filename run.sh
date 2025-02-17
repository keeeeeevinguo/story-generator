#!/bin/bash

# Install requirements
(pip install -r server/requirements.txt) &

wait

# Install the required packages
(cd client && npm install) &

wait

# Start the Vue.js frontend
(cd client && npm run dev) &

# Start the Sanic backend
(cd server && python app.py) &

# Wait for both processes to exit
wait
