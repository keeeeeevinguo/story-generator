# Storybook Generator

Storybook Generator is a web application that creates children's stories based on user input. The application features a Vue.js frontend for a responsive user interface and a Sanic (Python) backend that generates stories using the Anthropic API.

## Purpose

This project is a mock-up to explore the potential for AI to generate personalized stories based on kids' interests. By tailoring stories to individual interests and incorporating specific vocabulary words, the program aims to make learning engaging and fun.

## Features

- **User Input:** Enter a topic or prompt for the story
- **Custom Settings:** Select a reading grade level, specify vocabulary words, and choose a genre
- **Story Generation:** Generates a complete children's story tailored to the given parameters
- **Responsive UI:** A Vue.js interface with a hamburger menu for settings
- **Integrated Database:** A MySQL database that allows users to save, retrieve and delete generated stories

## Project Set Up

1. Clone the repository using `git clone`

2. Create a `.env` file in the root directory with your API key, MYSQL username, password, host, and database name

3. Run `./run.sh` to start up the frontend and backend
