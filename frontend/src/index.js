import React from "react";
import { createRoot } from "react-dom/client";
import { Provider } from "react-redux"; // Import Provider
import store from "./store/store"; // Import your Redux store
import "./index.css";
import App from "./App";

const container = document.getElementById("root");
const root = createRoot(container);

root.render(
  <Provider store={store}>
    {" "}
    {/* Wrap your App with Provider */}
    <App />
  </Provider>
);
