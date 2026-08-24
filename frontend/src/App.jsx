import { useEffect, useMemo, useState } from "react";
import "./index.css";

const API_URL = "http://127.0.0.1:8000";

const recommendationTemplates = {
  Microchip: [
    {
      option: "Air Freight",
      cost: 15000,
      delay: 2,
      risk: "Low",
      score: 92,
      description: "Fastest recovery option for critical inventory.",
    },
    {
      option: "Secondary Supplier",
      cost: 12000,
      delay: 4,
      risk: "Medium",
      score: 78,
      description: "Balanced option between cost and delivery speed.",
    },
    {
      option: "Delay Product Launch",
      cost: 2000,
      delay: 14,
      risk: "High",
      score: 48,
      description: "Lowest cost, but creates a significant delay.",
    },
  ],

  Monitor: [
    {
      option: "Air Freight",
      cost: 11000,
      delay: 2,
      risk: "Low",
      score: 91,
      description: "Quickest option for maintaining customer commitments.",
    },
    {
      option: "Secondary Supplier",
      cost: 8500,
      delay: 5,
      risk: "Medium",
      score: 76,
      description: "Good balance of operational cost and speed.",
    },
    {
      option: "Delay Product Launch",
      cost: 1800,
      delay: 12,
      risk: "High",
      score: 46,
      description: "Saves cost but introduces substantial delivery risk.",
    },
  ],

  Keyboard: [
    {
      option: "Air Freight",
      cost: 9000,
      delay: 2,
      risk: "Low",
      score: 89,
      description: "Fast recovery for keyboard inventory shortages.",
    },
    {
      option: "Secondary Supplier",
      cost: 7000,
      delay: 4,
      risk: "Medium",
      score: 74,
      description: "Moderate cost with acceptable delivery speed.",
    },
    {
      option: "Delay Product Launch",
      cost: 1500,
      delay: 10,
      risk: "High",
      score: 44,
      description: "Cheapest option but significantly increases delay.",
    },
  ],
};

const defaultRecommendations = [
  {
    option: "Air Freight",
    cost: 15000,
    delay: 2,
    risk: "Low",
    score: 92,
    description: "Fastest recovery option.",
  },
  {
    option: "Secondary Supplier",
    cost: 12000,
    delay: 4,
    risk: "Medium",
    score: 78,
    description: "Balanced cost and speed.",
  },
  {
    option: "Delay Product Launch",
    cost: 2000,
    delay: 14,
    risk: "High",
    score: 48,
    description: "Lowest cost but highest delay.",
  },
];

function getRisk(shipment) {
  if (!shipment) return "LOW";

  const inventory = Number(shipment.inventory_level || 0);
  const quantity = Number(shipment.quantity || 0);

  if (inventory < quantity * 0.2) {
    return "HIGH";
  }

  if (inventory < quantity * 0.5) {
    return "MEDIUM";
  }

  return "LOW";
}

function getRiskClass(risk) {
  const value = String(risk || "").toLowerCase();

  if (value === "high") return "risk-high";
  if (value === "medium") return "risk-medium";
  return "risk-low";
}

function formatDate(dateValue) {
  if (!dateValue) return "—";

  const date = new Date(dateValue);

  if (Number.isNaN(date.getTime())) {
    return String(dateValue);
  }

  return date.toLocaleDateString("en-IN", {
    day: "2-digit",
    month: "short",
    year: "numeric",
  });
}

function formatCurrency(value) {
  return new Intl.NumberFormat("en-US", {
    style: "currency",
    currency: "USD",
    maximumFractionDigits: 0,
  }).format(Number(value || 0));
}

function App() {
  const [shipments, setShipments] = useState([]);
  const [selectedProduct, setSelectedProduct] = useState("");
  const [selectedShipment, setSelectedShipment] = useState(null);

  const [loading, setLoading] = useState(true);
  const [error, setError] = useState("");

  const [activePage, setActivePage] = useState("dashboard");
  const [executedOption, setExecutedOption] = useState(null);
  const [showNotifications, setShowNotifications] = useState(false);

  useEffect(() => {
    loadShipments();
  }, []);

  async function loadShipments() {
    try {
      setLoading(true);
      setError("");

      const response = await fetch(`${API_URL}/shipments/`);

      if (!response.ok) {
        throw new Error(`Server returned ${response.status}`);
      }

      const data = await response.json();

      console.log("Shipments received:", data);

      setShipments(Array.isArray(data) ? data : []);

      if (Array.isArray(data) && data.length > 0) {
        setSelectedProduct(data[0].product);
      }
    } catch (err) {
      console.error(err);
      setError(
        "Unable to connect to the FastAPI backend. Make sure the backend is running on port 8000."
      );
    } finally {
      setLoading(false);
    }
  }

  const products = useMemo(() => {
    return [...new Set(shipments.map((item) => item.product).filter(Boolean))];
  }, [shipments]);

  const productShipments = useMemo(() => {
    if (!selectedProduct) return shipments;

    return shipments.filter(
      (item) =>
        String(item.product).toLowerCase() ===
        String(selectedProduct).toLowerCase()
    );
  }, [shipments, selectedProduct]);

  useEffect(() => {
    if (productShipments.length > 0) {
      setSelectedShipment(productShipments[0]);
    } else {
      setSelectedShipment(null);
    }
  }, [productShipments]);

  const recommendations =
    recommendationTemplates[selectedProduct] || defaultRecommendations;

  const activeShipments = shipments.length;

  const totalQuantity = shipments.reduce(
    (sum, shipment) => sum + Number(shipment.quantity || 0),
    0
  );

  const highRiskCount = shipments.filter(
    (shipment) => getRisk(shipment) === "HIGH"
  ).length;

  const selectedRisk = getRisk(selectedShipment);

  function executeDecision(option) {
    setExecutedOption(option);

    setTimeout(() => {
      setExecutedOption(null);
    }, 3000);
  }

  return (
    <div className="app-shell">
      {/* SIDEBAR */}
      <aside className="sidebar">
        <div className="brand">
          <div className="brand-logo">
            <span>✦</span>
          </div>

          <div className="brand-text">
            <strong>SUPPLY</strong>
            <strong>PRESCRIPT</strong>
          </div>
        </div>

        <nav className="side-nav">
          <button
            className={`nav-item ${
              activePage === "dashboard" ? "active" : ""
            }`}
            onClick={() => setActivePage("dashboard")}
          >
            <span className="nav-icon">⌂</span>
            <span>Dashboard</span>
          </button>

          <button
            className={`nav-item ${
              activePage === "shipments" ? "active" : ""
            }`}
            onClick={() => setActivePage("shipments")}
          >
            <span className="nav-icon">◈</span>
            <span>Shipments</span>
          </button>

          <button
            className={`nav-item ${
              activePage === "recommendations" ? "active" : ""
            }`}
            onClick={() => setActivePage("recommendations")}
          >
            <span className="nav-icon">✦</span>
            <span>Prescriptions</span>
          </button>

          <button
            className={`nav-item ${
              activePage === "analytics" ? "active" : ""
            }`}
            onClick={() => setActivePage("analytics")}
          >
            <span className="nav-icon">▥</span>
            <span>Analytics</span>
          </button>
        </nav>

        <div className="sidebar-bottom">
          <button className="nav-item">
            <span className="nav-icon">⚙</span>
            <span>Settings</span>
          </button>

          <div className="sidebar-status">
            <span className="status-dot"></span>
            <span>System Online</span>
          </div>
        </div>
      </aside>

      {/* MAIN */}
      <main className="main-area">
        {/* HEADER */}
        <header className="topbar">
          <div>
            <div className="breadcrumb">SUPPLY CHAIN / INTELLIGENCE</div>

            <h1>Supply Prescript</h1>

            <p>
              Predictive supply chain intelligence and prescriptive
              recommendations.
            </p>
          </div>

          <div className="topbar-actions">
            <button
              className="icon-button"
              onClick={() => setShowNotifications(!showNotifications)}
            >
              ♧
              {highRiskCount > 0 && (
                <span className="notification-dot">{highRiskCount}</span>
              )}
            </button>

            <button className="refresh-button" onClick={loadShipments}>
              ↻ Refresh
            </button>

            <div className="profile">
              <div className="avatar">SP</div>

              <div>
                <strong>Supply Manager</strong>
                <span>Operations</span>
              </div>
            </div>
          </div>

          {showNotifications && (
            <div className="notification-panel">
              <strong>System notifications</strong>

              <p>
                {highRiskCount > 0
                  ? `${highRiskCount} shipment requires attention.`
                  : "No high-risk shipments detected."}
              </p>
            </div>
          )}
        </header>

        {error && (
          <div className="error-banner">
            <div>
              <strong>Backend connection problem</strong>
              <span>{error}</span>
            </div>

            <button onClick={loadShipments}>Retry</button>
          </div>
        )}

        {loading ? (
          <div className="loading-screen">
            <div className="loader"></div>
            <p>Loading supply chain intelligence...</p>
          </div>
        ) : (
          <>
            {/* DASHBOARD */}
            <section className="content">
              <div className="page-heading">
                <div>
                  <span className="eyebrow">OPERATIONS OVERVIEW</span>
                  <h2>Control Center</h2>
                  <p>
                    Monitor shipments, identify risks and execute optimized
                    decisions.
                  </p>
                </div>

                {/* PRODUCT DROPDOWN */}
                <div className="product-selector">
                  <label>PRODUCT</label>

                  <select
                    value={selectedProduct}
                    onChange={(event) =>
                      setSelectedProduct(event.target.value)
                    }
                  >
                    {products.length === 0 ? (
                      <option value="">No products</option>
                    ) : (
                      products.map((product) => (
                        <option key={product} value={product}>
                          {product}
                        </option>
                      ))
                    )}
                  </select>
                </div>
              </div>

              {/* KPI CARDS */}
              <div className="kpi-grid">
                <KpiCard
                  label="Active Shipments"
                  value={activeShipments}
                  icon="◈"
                  trend="+12%"
                />

                <KpiCard
                  label="High Risk"
                  value={highRiskCount}
                  icon="△"
                  trend={highRiskCount > 0 ? "Attention" : "Stable"}
                  danger={highRiskCount > 0}
                />

                <KpiCard
                  label="Total Quantity"
                  value={totalQuantity.toLocaleString()}
                  icon="▦"
                  trend="Units"
                />

                <KpiCard
                  label="System Status"
                  value="ONLINE"
                  icon="●"
                  trend="Operational"
                  online
                />
              </div>

              {/* MAIN ANALYTICS GRID */}
              <div className="analytics-grid">
                {/* COST SPEED CHART */}
                <section className="panel chart-panel">
                  <div className="panel-header">
                    <div>
                      <span className="eyebrow">DECISION ANALYTICS</span>
                      <h3>Cost vs Speed</h3>
                      <p>
                        Compare recommendation options across cost and expected
                        delay.
                      </p>
                    </div>

                    <div className="chart-legend">
                      <span>
                        <i className="legend-purple"></i> Selected
                      </span>
                      <span>
                        <i className="legend-pink"></i> Alternatives
                      </span>
                    </div>
                  </div>

                  <CostSpeedChart recommendations={recommendations} />
                </section>

                {/* SELECTED SHIPMENT */}
                <section className="panel shipment-panel">
                  <div className="panel-header">
                    <div>
                      <span className="eyebrow">SELECTED SHIPMENT</span>
                      <h3>
                        {selectedShipment?.shipment_id || "No shipment"}
                      </h3>
                    </div>

                    <span className={`risk-pill ${getRiskClass(selectedRisk)}`}>
                      {selectedRisk}
                    </span>
                  </div>

                  {selectedShipment ? (
                    <div className="shipment-detail">
                      <div className="shipment-product">
                        <div className="product-icon">◈</div>

                        <div>
                          <strong>{selectedShipment.product}</strong>
                          <span>
                            Supplier {selectedShipment.supplier_id || "—"}
                          </span>
                        </div>
                      </div>

                      <div className="detail-grid">
                        <Detail
                          label="Origin"
                          value={selectedShipment.origin}
                        />

                        <Detail
                          label="Destination"
                          value={selectedShipment.destination}
                        />

                        <Detail
                          label="Quantity"
                          value={selectedShipment.quantity}
                        />

                        <Detail
                          label="Inventory"
                          value={selectedShipment.inventory_level}
                        />

                        <Detail
                          label="Expected Delivery"
                          value={formatDate(
                            selectedShipment.expected_delivery_date
                          )}
                        />

                        <Detail
                          label="Delay Probability"
                          value={`${selectedRisk === "HIGH" ? 87 : selectedRisk === "MEDIUM" ? 55 : 22}%`}
                        />
                      </div>

                      <div className={`risk-alert ${getRiskClass(selectedRisk)}`}>
                        <span>△</span>

                        <div>
                          <strong>Delay Risk: {selectedRisk}</strong>
                          <p>
                            Supply chain conditions are being monitored for
                            this shipment.
                          </p>
                        </div>
                      </div>
                    </div>
                  ) : (
                    <div className="empty-state">
                      Select a product to view shipment details.
                    </div>
                  )}
                </section>
              </div>

              {/* RECOMMENDATIONS */}
              <section className="recommendations-section">
                <div className="section-title">
                  <div>
                    <span className="eyebrow">AI PRESCRIPTION</span>

                    <h2>Recommended Actions</h2>

                    <p>
                      Optimized decisions for{" "}
                      <strong>{selectedProduct || "selected product"}</strong>
                    </p>
                  </div>

                  <div className="ai-badge">
                    <span>✦</span>
                    AI OPTIMIZED
                  </div>
                </div>

                <div className="recommendation-grid">
                  {recommendations.map((recommendation, index) => (
                    <RecommendationCard
                      key={recommendation.option}
                      recommendation={recommendation}
                      index={index}
                      selected={index === 0}
                      executed={executedOption === recommendation.option}
                      onExecute={() => executeDecision(recommendation.option)}
                    />
                  ))}
                </div>
              </section>

              {/* SHIPMENT TABLE */}
              <section className="panel shipments-table-panel">
                <div className="panel-header">
                  <div>
                    <span className="eyebrow">LIVE DATA</span>
                    <h3>Shipment Monitor</h3>
                  </div>

                  <span className="live-indicator">
                    <i></i> LIVE
                  </span>
                </div>

                <div className="table-wrapper">
                  <table>
                    <thead>
                      <tr>
                        <th>Shipment</th>
                        <th>Product</th>
                        <th>Route</th>
                        <th>Quantity</th>
                        <th>Inventory</th>
                        <th>Risk</th>
                        <th>Delivery</th>
                      </tr>
                    </thead>

                    <tbody>
                      {shipments.map((shipment) => {
                        const risk = getRisk(shipment);

                        return (
                          <tr
                            key={shipment.shipment_id}
                            className={
                              selectedShipment?.shipment_id ===
                              shipment.shipment_id
                                ? "selected-row"
                                : ""
                            }
                            onClick={() => {
                              setSelectedProduct(shipment.product);
                              setSelectedShipment(shipment);
                            }}
                          >
                            <td>
                              <strong>{shipment.shipment_id}</strong>
                            </td>

                            <td>{shipment.product}</td>

                            <td>
                              {shipment.origin} → {shipment.destination}
                            </td>

                            <td>{shipment.quantity}</td>

                            <td>{shipment.inventory_level}</td>

                            <td>
                              <span
                                className={`table-risk ${getRiskClass(risk)}`}
                              >
                                {risk}
                              </span>
                            </td>

                            <td>
                              {formatDate(shipment.expected_delivery_date)}
                            </td>
                          </tr>
                        );
                      })}
                    </tbody>
                  </table>
                </div>
              </section>
            </section>
          </>
        )}
      </main>
    </div>
  );
}

/* -------------------------------- */
/* KPI CARD                         */
/* -------------------------------- */

function KpiCard({
  label,
  value,
  icon,
  trend,
  danger,
  online,
}) {
  return (
    <div className="kpi-card">
      <div className="kpi-top">
        <div className="kpi-icon">{icon}</div>

        <span className={danger ? "trend danger" : "trend"}>
          {trend}
        </span>
      </div>

      <span className="kpi-label">{label}</span>

      <strong className={online ? "kpi-value online" : "kpi-value"}>
        {value}
      </strong>

      <div className="kpi-glow"></div>
    </div>
  );
}

/* -------------------------------- */
/* DETAIL                           */
/* -------------------------------- */

function Detail({ label, value }) {
  return (
    <div className="detail">
      <span>{label}</span>
      <strong>{value || "—"}</strong>
    </div>
  );
}

/* -------------------------------- */
/* RECOMMENDATION CARD              */
/* -------------------------------- */

function RecommendationCard({
  recommendation,
  index,
  selected,
  executed,
  onExecute,
}) {
  return (
    <div
      className={`recommendation-card ${
        selected ? "recommended" : ""
      }`}
    >
      {selected && (
        <div className="recommended-label">
          <span>✦</span> BEST OPTION
        </div>
      )}

      <div className="recommendation-number">
        0{index + 1}
      </div>

      <div className="recommendation-icon">
        {index === 0 ? "✈" : index === 1 ? "◆" : "◷"}
      </div>

      <h3>{recommendation.option}</h3>

      <p className="recommendation-description">
        {recommendation.description}
      </p>

      <div className="recommendation-stats">
        <div>
          <span>COST</span>
          <strong>{formatCurrency(recommendation.cost)}</strong>
        </div>

        <div>
          <span>DELAY</span>
          <strong>{recommendation.delay} days</strong>
        </div>

        <div>
          <span>RISK</span>
          <strong className={getRiskClass(recommendation.risk)}>
            {recommendation.risk}
          </strong>
        </div>
      </div>

      <div className="score-section">
        <div className="score-header">
          <span>DECISION SCORE</span>
          <strong>{recommendation.score}%</strong>
        </div>

        <div className="score-bar">
          <div
            style={{
              width: `${recommendation.score}%`,
            }}
          ></div>
        </div>
      </div>

      <button
        className={`execute-button ${executed ? "executed" : ""}`}
        onClick={onExecute}
      >
        {executed ? "✓ DECISION EXECUTED" : "EXECUTE DECISION →"}
      </button>
    </div>
  );
}

/* -------------------------------- */
/* COST VS SPEED CHART              */
/* -------------------------------- */

function CostSpeedChart({ recommendations }) {
  const maxCost = Math.max(
    ...recommendations.map((item) => item.cost),
    1
  );

  const maxDelay = Math.max(
    ...recommendations.map((item) => item.delay),
    1
  );

  return (
    <div className="cost-speed-chart">
      <div className="chart-y-label">SPEED</div>

      <div className="chart-area">
        <div className="grid-line horizontal one"></div>
        <div className="grid-line horizontal two"></div>
        <div className="grid-line horizontal three"></div>
        <div className="grid-line horizontal four"></div>

        <div className="grid-line vertical one"></div>
        <div className="grid-line vertical two"></div>
        <div className="grid-line vertical three"></div>
        <div className="grid-line vertical four"></div>

        {recommendations.map((item, index) => {
          const x =
            10 + (item.cost / maxCost) * 78;

          const y =
            90 - (1 - item.delay / maxDelay) * 72;

          return (
            <div
              key={item.option}
              className={`chart-point point-${index}`}
              style={{
                left: `${Math.min(x, 88)}%`,
                top: `${Math.max(8, Math.min(y, 88))}%`,
              }}
            >
              <span className="point-dot"></span>

              <div className="point-tooltip">
                <strong>{item.option}</strong>
                <span>{formatCurrency(item.cost)}</span>
                <span>{item.delay} days</span>
              </div>

              <span className="point-label">
                {item.option}
              </span>
            </div>
          );
        })}

        <div className="axis-x"></div>
        <div className="axis-y"></div>

        <span className="axis-label x-left">LOW COST</span>
        <span className="axis-label x-right">HIGH COST</span>

        <span className="axis-label y-top">FAST</span>
        <span className="axis-label y-bottom">SLOW</span>
      </div>
    </div>
  );
}

export default App;