import { useEffect, useState } from "react";
import "./App.css";

const API_URL = "http://127.0.0.1:8000";

function App() {
  const [shipments, setShipments] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState("");

  useEffect(() => {
    fetchShipments();
  }, []);

  const fetchShipments = async () => {
    try {
      setLoading(true);
      setError("");

      const response = await fetch(`${API_URL}/shipments/`);

      if (!response.ok) {
        throw new Error("Failed to fetch shipments");
      }

      const data = await response.json();
      setShipments(data);
    } catch (err) {
      console.error(err);
      setError(
        "Unable to connect to the backend. Make sure FastAPI is running on port 8000."
      );
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="app">
      {/* Header */}
      <header className="header">
        <div>
          <h1>SUPPLY PRESCRIPT</h1>
          <p>Supply Chain Intelligence Dashboard</p>
        </div>

        <button className="refresh-btn" onClick={fetchShipments}>
          ↻ Refresh
        </button>
      </header>

      {/* Main */}
      <main className="dashboard">
        <section className="page-title">
          <h2>Active Supply Chain Alerts</h2>
          <p>Monitor shipments, delays and operational risks.</p>
        </section>

        {/* Summary cards */}
        <section className="summary-grid">
          <div className="summary-card">
            <span>Active Shipments</span>
            <strong>{shipments.length}</strong>
          </div>

          <div className="summary-card warning">
            <span>High Risk</span>
            <strong>
              {shipments.filter((shipment) => shipment.inventory_level < 20)
                .length}
            </strong>
          </div>

          <div className="summary-card">
            <span>Total Quantity</span>
            <strong>
              {shipments.reduce(
                (total, shipment) =>
                  total + Number(shipment.quantity || 0),
                0
              )}
            </strong>
          </div>

          <div className="summary-card">
            <span>System Status</span>
            <strong className="status">ONLINE</strong>
          </div>
        </section>

        {/* Error */}
        {error && (
          <div className="error-box">
            <strong>Connection Error</strong>
            <p>{error}</p>
          </div>
        )}

        {/* Loading */}
        {loading && (
          <div className="loading">
            Loading shipment data...
          </div>
        )}

        {/* Shipment alerts */}
        {!loading && !error && shipments.length > 0 && (
          <section className="alerts">
            <h2>Shipment Alerts</h2>

            {shipments.map((shipment) => {
              const inventory = Number(shipment.inventory_level || 0);

              let risk = "LOW";

              if (inventory < 20) {
                risk = "HIGH";
              } else if (inventory < 50) {
                risk = "MEDIUM";
              }

              return (
                <div className="shipment-card" key={shipment.shipment_id}>
                  <div className="shipment-header">
                    <div>
                      <h3>Shipment {shipment.shipment_id}</h3>
                      <p>{shipment.product}</p>
                    </div>

                    <span className={`risk ${risk.toLowerCase()}`}>
                      {risk}
                    </span>
                  </div>

                  <div className="shipment-details">
                    <div>
                      <span>Supplier</span>
                      <strong>{shipment.supplier_id}</strong>
                    </div>

                    <div>
                      <span>Origin</span>
                      <strong>{shipment.origin}</strong>
                    </div>

                    <div>
                      <span>Destination</span>
                      <strong>{shipment.destination}</strong>
                    </div>

                    <div>
                      <span>Quantity</span>
                      <strong>{shipment.quantity}</strong>
                    </div>

                    <div>
                      <span>Inventory</span>
                      <strong>{shipment.inventory_level}</strong>
                    </div>

                    <div>
                      <span>Expected Delivery</span>
                      <strong>
                        {shipment.expected_delivery_date
                          ? new Date(
                              shipment.expected_delivery_date
                            ).toLocaleDateString()
                          : "N/A"}
                      </strong>
                    </div>
                  </div>

                  <div className="alert-message">
                    ⚠ Delay Risk: <strong>{risk}</strong>
                  </div>
                </div>
              );
            })}
          </section>
        )}

        {/* Empty */}
        {!loading && !error && shipments.length === 0 && (
          <div className="empty">
            No shipments found in the database.
          </div>
        )}
      </main>
    </div>
  );
}

export default App;