import React, { useState } from "react";
import axios from "axios";
import "./App.css";

const API_BASE = "https://qest-multiagent-production.up.railway.app/";

// Info Card Renderers
function ClientCard({ client }) {
  return (
    <div className="info-card" key={client._id}>
      <div className="info-card__row">
        <span className="info-label">Name:</span>
        <span className="info-value">{client.name}</span>
      </div>
      <div className="info-card__row">
        <span className="info-label">Email:</span>
        <span className="info-value">{client.email}</span>
      </div>
      <div className="info-card__row">
        <span className="info-label">Phone:</span>
        <span className="info-value">{client.phone}</span>
      </div>
      <div className="info-card__row">
        <span className="info-label">Status:</span>
        <span className="info-value">{client.status}</span>
      </div>
      <div className="info-card__row">
        <span className="info-label">DOB:</span>
        <span className="info-value">{client.dob}</span>
      </div>
      <div className="info-card__row">
        <span className="info-label">Created At:</span>
        <span className="info-value">{client.created_at}</span>
      </div>
      <div className="info-card__row">
        <span className="info-label">Enrolled Services:</span>
        <span className="info-value">
          {client.enrolled_services && client.enrolled_services.length > 0
            ? client.enrolled_services.join(", ")
            : "None"}
        </span>
      </div>
    </div>
  );
}

function OrderCard({ order }) {
  return (
    <div className="info-card" key={order._id}>
      <div className="info-card__row">
        <span className="info-label">Order ID:</span>
        <span className="info-value">{order._id}</span>
      </div>
      <div className="info-card__row">
        <span className="info-label">Client ID:</span>
        <span className="info-value">{order.client_id}</span>
      </div>
      <div className="info-card__row">
        <span className="info-label">Service:</span>
        <span className="info-value">{order.service}</span>
      </div>
      <div className="info-card__row">
        <span className="info-label">Status:</span>
        <span className="info-value">{order.status}</span>
      </div>
      <div className="info-card__row">
        <span className="info-label">Amount:</span>
        <span className="info-value">{order.amount}</span>
      </div>
      <div className="info-card__row">
        <span className="info-label">Created At:</span>
        <span className="info-value">{order.created_at}</span>
      </div>
    </div>
  );
}

function ClassCard({ klass }) {
  return (
    <div className="info-card" key={klass._id || klass.date}>
      <div className="info-card__row">
        <span className="info-label">Course ID:</span>
        <span className="info-value">{klass.course_id}</span>
      </div>
      <div className="info-card__row">
        <span className="info-label">Date:</span>
        <span className="info-value">{klass.date}</span>
      </div>
      <div className="info-card__row">
        <span className="info-label">Instructor:</span>
        <span className="info-value">{klass.instructor}</span>
      </div>
      <div className="info-card__row">
        <span className="info-label">Status:</span>
        <span className="info-value">{klass.status}</span>
      </div>
    </div>
  );
}

function PaymentCard({ payment }) {
  return (
    <div className="info-card" key={payment._id || payment.order_id}>
      <div className="info-card__row">
        <span className="info-label">Order ID:</span>
        <span className="info-value">{payment.order_id}</span>
      </div>
      <div className="info-card__row">
        <span className="info-label">Amount:</span>
        <span className="info-value">{payment.amount}</span>
      </div>
      <div className="info-card__row">
        <span className="info-label">Status:</span>
        <span className="info-value">{payment.status}</span>
      </div>
      <div className="info-card__row">
        <span className="info-label">Paid At:</span>
        <span className="info-value">{payment.paid_at}</span>
      </div>
    </div>
  );
}

// Main Response Renderer
function renderResponse(response) {
  if (response.clients && Array.isArray(response.clients)) {
    return (
      <div>
        <b>Clients:</b>
        {response.clients.map((client) => <ClientCard client={client} key={client._id} />)}
      </div>
    );
  }
  if (response.orders && Array.isArray(response.orders)) {
    return (
      <div>
        <b>Orders:</b>
        {response.orders.map((order) => <OrderCard order={order} key={order._id} />)}
      </div>
    );
  }
  if (response.classes && Array.isArray(response.classes)) {
    return (
      <div>
        <b>Classes:</b>
        {response.classes.map((klass, i) => <ClassCard klass={klass} key={klass._id || i} />)}
      </div>
    );
  }
  if (response.payments && Array.isArray(response.payments)) {
    return (
      <div>
        <b>Payments:</b>
        {response.payments.map((payment, i) => <PaymentCard payment={payment} key={payment._id || i} />)}
      </div>
    );
  }
  // Single-value responses as info cards
  if (response.total_revenue !== undefined) {
    return (
      <div className="info-card">
        <span className="info-label">Total Revenue This Month:</span>
        <span className="info-value">₹ {response.total_revenue}</span>
      </div>
    );
  }
  if (response.outstanding_payments !== undefined) {
    return (
      <div className="info-card">
        <span className="info-label">Outstanding Payments:</span>
        <span className="info-value">₹ {response.outstanding_payments}</span>
      </div>
    );
  }
  if (response.active_clients !== undefined) {
    return (
      <div className="info-card">
        <span className="info-label">Active Clients:</span>
        <span className="info-value">{response.active_clients}</span>
      </div>
    );
  }
  if (response.inactive_clients !== undefined) {
    return (
      <div className="info-card">
        <span className="info-label">Inactive Clients:</span>
        <span className="info-value">{response.inactive_clients}</span>
      </div>
    );
  }
  if (response.paid !== undefined && response.order_id) {
    return (
      <div className="info-card">
        <span className="info-label">Order #{response.order_id} Paid:</span>
        <span className="info-value">{response.paid ? "Yes" : "No"}</span>
      </div>
    );
  }
  // Fallback: pretty print JSON
  return (
    <pre className="json-pretty">
      {JSON.stringify(response, null, 2)}
    </pre>
  );
}

function App() {
  const [agent, setAgent] = useState("support");
  const [query, setQuery] = useState("");
  const [response, setResponse] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");

  const handleSubmit = async (e) => {
    e.preventDefault();
    setError("");
    setResponse(null);
    setLoading(true);

    try {
      const res = await axios.post(
        `${API_BASE}/${agent}/query`,
        { query },
        { headers: { "Content-Type": "application/json" } }
      );
      setResponse(res.data);
    } catch (err) {
      setError(
        err.response?.data?.error ||
        err.message ||
        "Unknown error occurred"
      );
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="app-container">
      <h1>Multi-Agent Query Interface</h1>
      <form onSubmit={handleSubmit}>
        <label>
          <b>Select Agent:</b>
          <select
            className="select"
            value={agent}
            onChange={(e) => setAgent(e.target.value)}
            style={{ marginLeft: 10 }}
          >
            <option value="support">Support Agent</option>
            <option value="dashboard">Dashboard Agent</option>
          </select>
        </label>
        <br /><br />
        <label>
          <b>Enter your query:</b>
          <textarea
            className="textarea"
            value={query}
            onChange={(e) => setQuery(e.target.value)}
            rows={3}
            style={{ width: "100%", marginTop: 8 }}
            placeholder={
              agent === "support"
                ? "e.g. What classes are available this week?"
                : "e.g. How much revenue did we generate this month?"
            }
            required
          />
        </label>
        <br />
        <button className="button" type="submit" disabled={loading}>
          {loading ? "Loading..." : "Send"}
        </button>
      </form>
      {error && (
        <div className="error-block">
          <b>Error:</b> {error}
        </div>
      )}
      {response && (
        <div className="response-block">
          <b>Response:</b>
          {renderResponse(response)}
        </div>
      )}
    </div>
  );
}

export default App;
