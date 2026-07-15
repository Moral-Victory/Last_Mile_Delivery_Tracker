# Basic Delivery Tracker

A simple, lightweight, and pure static single-page application (SPA) to log and manage local delivery orders.

## Features
- **Create**: Add new delivery orders with pickup address, dropoff address, weight, and status.
- **Read**: View all logged orders in a simple structured table.
- **Update**: Edit the delivery status of any order dynamically.
- **Delete**: Cancel or remove orders from the tracker.
- **Local Storage Persistence**: Uses the browser's `localStorage` to save your orders. Your data will remain intact even if you refresh or close the page.

## How to Run
Since this application has no backend, database setup, or external dependencies, running it is extremely simple:
1. Double-click the `index.html` file to open it in any modern web browser.
2. Alternatively, open your browser and drag the `index.html` file into the window.

## Architecture
- **Structure**: Vanilla HTML5
- **Style**: Basic inline CSS
- **Logic**: Vanilla client-side JavaScript
- **Database**: Serialized JSON objects stored inside browser `localStorage`
