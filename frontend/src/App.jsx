import { useEffect, useMemo, useState } from "react";
import "./App.css";

const API_URL = "http://127.0.0.1:8000";
const recommendationTemplates = {
  Microchip: [
  {
  recommendation_id: "R001",
  option: "Air Freight",
  cost: 15000,
  delay: 2,
  risk: "Low",
  score: 92,
  description: "Fastest recovery option for critical inventory.",
  },
  {
  recommendation_id: "R002",
  option: "Secondary Supplier",
  cost: 12000,
  delay: 4,
  risk: "Medium",
  score: 78,
  description: "Balanced option between cost and delivery speed.",
  },
  {
  recommendation_id: "R003",
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
  recommendation_id: "R001",
  option: "Air Freight",
  cost: 11000,
  delay: 2,
  risk: "Low",
  score: 91,
  description: "Quickest option for maintaining customer commitments.",
},
{
  recommendation_id: "R002",
  option: "Secondary Supplier",
  cost: 8500,
  delay: 5,
  risk: "Medium",
  score: 76,
  description: "Good balance of operational cost and speed.",
},
{
  recommendation_id: "R003",
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
  recommendation_id: "R001",
  option: "Air Freight",
  cost: 9000,
  delay: 2,
  risk: "Low",
  score: 89,
  description: "Fast recovery for keyboard inventory shortages.",
},
{
  recommendation_id: "R002",
  option: "Secondary Supplier",
  cost: 7000,
  delay: 4,
  risk: "Medium",
  score: 74,
  description: "Moderate cost with acceptable delivery speed.",
},
{
  recommendation_id: "R003",
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

  const [decisions, setDecisions] = useState([]);
  const [selectedDecision, setSelectedDecision] = useState([]);
  const [analyticsLoading, setAnalyticsLoading] = useState(false);
  const [showAnalytics, setShowAnalytics] = useState(false);

  const [feedbackResult, setFeedbackResult] = useState(null);
  const [workflowStep, setWorkflowStep] = useState(1);
  const [executedOption, setExecutedOption] = useState(null);
  const [showNotifications, setShowNotifications] = useState(false);
  const [lastExecutedDecision, setLastExecutedDecision] = useState(null);
const submitFeedback = async (
  decisionId,
  outcome,
  actualCost,
  actualDelay,
  success,
  feedbackNote
) => {
  try {
    console.log("Submitting feedback:", {
      decision_id: decisionId,
      outcome,
      actual_cost: actualCost,
      actual_delay: actualDelay,
      success,
      feedback_note: feedbackNote,
    });

    const response = await fetch(
      `${API_URL}/feedback/`,
      {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({
          decision_id: decisionId,
          outcome,
          actual_cost: actualCost,
          actual_delay: actualDelay,
          success,
          feedback_note: feedbackNote,
        }),
      }
    );

    const data = await response.json();

    console.log("Feedback response status:", response.status);
    console.log("Feedback recorded:", data);

    setFeedbackResult({
  outcome,
  actualCost,
  actualDelay,
  success,
  feedbackNote,
});

  setWorkflowStep(8);

    if (!response.ok) {
      throw new Error(
        typeof data.detail === "string"
          ? data.detail
          : JSON.stringify(data.detail) || "Failed to submit feedback"
      );
    }

    alert("Feedback recorded successfully!");

  } catch (error) {
    console.error("Feedback error:", error);

    alert(`Failed to record feedback: ${error.message}`);
  }
};
  useEffect(() => {
    loadShipments();
  }, []);
  async function fetchDecisions() {
  try {
    setAnalyticsLoading(true);

    const response = await fetch(`${API_URL}/decisions/`);

    if (!response.ok) {
      throw new Error("Failed to fetch decisions");
    }

    const data = await response.json();

    console.log("Decisions received:", data);

    setDecisions(Array.isArray(data) ? data : []);

  } catch (error) {
    console.error("Failed to load decisions:", error);
  } finally {
    setAnalyticsLoading(false);
  }
}
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
      if (showAnalytics) {
        fetchDecisions();
  }
}, [showAnalytics]);
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
async function executeDecision(recommendation) {
  if (!selectedShipment) {
    setError("Please select a shipment before executing a decision.");
    return;
  }

  try {
    setError("");

    console.log("Executing decision:", {
      shipment_id: selectedShipment.shipment_id,
      product: selectedShipment.product,
      recommendation_id: recommendation.recommendation_id,
      selected_action: recommendation.option,
    });

    const response = await fetch(`${API_URL}/decisions/`, {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify({
        shipment_id: selectedShipment.shipment_id,
        recommendation_id: recommendation.recommendation_id,
        selected_action: recommendation.option,
        predicted_cost: recommendation.cost,
        predicted_delay: recommendation.delay,
        decision_status: "EXECUTED",
      }),
    });

    const data = await response.json();

    console.log("Decision API status:", response.status);
    console.log("Decision API response:", data);

    if (!response.ok) {
      throw new Error(
        typeof data.detail === "string"
          ? data.detail
          : JSON.stringify(data.detail) || "Failed to execute decision."
      );
    }

    console.log("Decision executed successfully:", data);
    setLastExecutedDecision({
      decisionId: data.decision_id,
      shipmentId: selectedShipment.shipment_id,
      recommendation: recommendation.option,
      recommendationId: recommendation.recommendation_id,
    });
    setWorkflowStep(6);
    setFeedbackResult(null);
    setExecutedOption(recommendation.option);
    await fetchDecisions();
    setTimeout(() => {
      setExecutedOption(null);
    }, 3000);

    // Refresh shipment/dashboard data
    await loadShipments();

  } catch (err) {
    console.error("Decision execution failed:", err);

    setError(
      err.message || "Unable to execute decision."
    );
  }
}
const totalDecisions = decisions.length;

// const successfulDecisions = decisions.filter(
//   (decision) =>
//     decision.status?.toUpperCase() === "EXECUTED"
// ).length;

// const successRate =
//   totalDecisions > 0
//     ? (successfulDecisions / totalDecisions) * 100
//     : 0;
const successfulDecisions = 0;

const successRate = 0;
const averagePredictedCost =
  totalDecisions > 0
    ? decisions.reduce(
        (sum, decision) =>
          sum + Number(decision.predicted_cost || 0),
        0
      ) / totalDecisions
    : 0;
  const actionCounts = decisions.reduce((acc, decision) => {
  const action = decision.selected_action || "Unknown";

  acc[action] = (acc[action] || 0) + 1;

  return acc;
}, {});
const actionUsage = Object.entries(actionCounts).map(
  ([action, count]) => ({
    action,
    count,
    percentage:
      totalDecisions > 0
        ? (count / totalDecisions) * 100
        : 0,
  })
);
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
            onClick={() => {
  setActivePage("dashboard");
  setShowAnalytics(false);
}}
          >
            <span className="nav-icon">⌂</span>
            <span>Dashboard</span>
          </button>

          <button
            className={`nav-item ${
              activePage === "shipments" ? "active" : ""
            }`}
            onClick={() => {setActivePage("shipments");
              setShowAnalytics(false);}
            }
          >
            <span className="nav-icon">◈</span>
            <span>Shipments</span>
          </button>

          <button
            className={`nav-item ${
              activePage === "recommendations" ? "active" : ""
            }`}
            onClick={() => {setActivePage("recommendations");
              setShowAnalytics(false);}
            }
          >
            <span className="nav-icon">✦</span>
            <span>Prescriptions</span>
          </button>

          <button
            className={`nav-item ${
              activePage === "analytics" ? "active" : ""
            }`}
              onClick={() => {
    setActivePage("analytics");
    setShowAnalytics(true);
  }}
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
        {/* Shipment Monitor */}
        {activePage === "shipments" && (
  <section className="page-screen">

    <div className="page-heading">
      <div>
        <span className="eyebrow">LIVE OPERATIONS</span>

        <h2>Shipment Monitor</h2>

        <p>
          Monitor active shipments and identify operational risks.
        </p>
      </div>
    </div>

    <section className="panel shipments-table-panel">

      <div className="panel-header">
        <div>
          <span className="eyebrow">LIVE DATA</span>
          <h3>All Shipments</h3>
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
                  onClick={() => {
                    setSelectedProduct(shipment.product);
                    setSelectedShipment(shipment);
                    setActivePage("dashboard");
                  }}
                >
                  <td>
                    <strong>{shipment.shipment_id}</strong>
                  </td>

                  <td>{shipment.product}</td>

                  <td>
                    {shipment.origin} →{" "}
                    {shipment.destination}
                  </td>

                  <td>{shipment.quantity}</td>

                  <td>{shipment.inventory_level}</td>

                  <td>
                    <span
                      className={`table-risk ${getRiskClass(
                        risk
                      )}`}
                    >
                      {risk}
                    </span>
                  </td>

                  <td>
                    {formatDate(
                      shipment.expected_delivery_date
                    )}
                  </td>
                </tr>
              );
            })}
          </tbody>
        </table>
      </div>

    </section>
  </section>
)}
{/* #Recommendation system */}
{activePage === "recommendations" && (
  <section className="page-screen">

    <div className="page-heading">
      <div>
        <span className="eyebrow">AI PRESCRIPTION</span>

        <h2>Recommended Actions</h2>

        <p>
          AI-generated recovery options for{" "}
          <strong>
            {selectedProduct || "selected product"}
          </strong>
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
          executed={
            executedOption === recommendation.option
          }
          onExecute={() =>
            executeDecision(recommendation)
          }
        />
      ))}
    </div>

  </section>
)}
      {lastExecutedDecision && (
        <div
        style={{
          marginBottom: "20px",
          padding: "16px 20px",
          borderRadius: "14px",
          border: "1px solid rgba(74, 222, 128, 0.2)",
          background: "rgba(74, 222, 128, 0.06)",
          display: "flex",
          alignItems: "center",
          justifyContent: "space-between",
          gap: "20px",
      }}
  >
        <div>
        <strong
        style={{
          display: "block",
          color: "#4ade80",
          fontSize: "12px",
          marginBottom: "5px",
        }}
      >
        ✓ DECISION EXECUTED
      </strong>

      <span
        style={{
          color: "var(--muted)",
          fontSize: "10px",
        }}
      >
        Shipment {lastExecutedDecision.shipmentId} →{" "}
        {lastExecutedDecision.recommendation}
      </span>
    </div>

    <span
      style={{
        color: "#4ade80",
        fontSize: "9px",
        fontWeight: 800,
        letterSpacing: "0.8px",
      }}
    >
      {lastExecutedDecision.recommendationId}
    </span>
  </div>
)}
        {loading ? (
          <div className="loading-screen">
            <div className="loader"></div>
            <p>Loading supply chain intelligence...</p>
          </div>
        ) : (
          <>
          {!showAnalytics && (
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
             <OperationalWorkflow
  selectedShipment={selectedShipment}
  selectedRisk={selectedRisk}
  recommendations={recommendations}
  lastExecutedDecision={lastExecutedDecision}
  feedbackResult={feedbackResult}
  workflowStep={workflowStep}
  setWorkflowStep={setWorkflowStep}
/> 
              {/* MAIN ANALYTICS GRID */}
              <div className="analytics-cards-grid decision-analytics-grid">
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
                        {lastExecutedDecision && (
  <div className="feedback-section">

    <div className="feedback-header">
      <div>
        <span className="eyebrow">TRACK OUTCOME</span>

        <h3>Decision Feedback</h3>

        <p>
          Tell us what happened after executing this recommendation.
        </p>
      </div>

      <span className="feedback-decision-id">
        {lastExecutedDecision.decisionId}
      </span>
    </div>

    <div className="feedback-actions">

      <button
        className="feedback-success"
        onClick={() =>
          submitFeedback(
            lastExecutedDecision.decisionId,
            "COMPLETED",
            14800,
            1,
            true,
            "Recommendation worked successfully"
          )
        }
      >
        <span>✓</span>
        OUTCOME SUCCESSFUL
      </button>

      <button
        className="feedback-failed"
        onClick={() =>
          submitFeedback(
            lastExecutedDecision.decisionId,
            "FAILED",
            17000,
            4,
            false,
            "Recommendation did not perform as expected"
          )
        }
      >
        <span>✕</span>
        OUTCOME FAILED
      </button>

    </div>

  </div>
)}
                      {feedbackResult && (
  <div className="outcome-result">

    <div className="outcome-result-header">
      <div>
        <span className="eyebrow">OUTCOME EVALUATION</span>
        <h3>Actual vs Predicted</h3>
      </div>

      <span
        className={
          feedbackResult.success
            ? "outcome-success"
            : "outcome-failed"
        }
      >
        {feedbackResult.success
          ? "✓ SUCCESS"
          : "✕ FAILED"}
      </span>
    </div>

    <div className="outcome-grid">

      <div className="outcome-metric">
        <span>PREDICTED COST</span>
        <strong>
          {formatCurrency(
            recommendations[0]?.cost || 0
          )}
        </strong>
      </div>

      <div className="outcome-metric">
        <span>ACTUAL COST</span>
        <strong>
          {formatCurrency(
            feedbackResult.actualCost
          )}
        </strong>
      </div>

      <div className="outcome-metric">
        <span>COST DIFFERENCE</span>
        <strong>
          {formatCurrency(
            feedbackResult.actualCost -
              (recommendations[0]?.cost || 0)
          )}
        </strong>
      </div>

      <div className="outcome-metric">
        <span>ACTUAL DELAY</span>
        <strong>
          {feedbackResult.actualDelay} days
        </strong>
      </div>

    </div>

    <p className="outcome-note">
      {feedbackResult.feedbackNote}
    </p>

  </div>
)}
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
                      onExecute={() => executeDecision(recommendation)}
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

              {showAnalytics && (
  <section className="analytics-dashboard">

    <div className="analytics-header">
      <div>
        <h1>Decision Analytics</h1>
        <p>
          Track decision performance and business outcomes.
        </p>
      </div>

      <button
        onClick={fetchDecisions}
        className="refresh-button"
        disabled={analyticsLoading}
      >
        {analyticsLoading ? "Loading..." : "Refresh"}
      </button>
    </div>


    {/* KPI CARDS */}

    <div className="analytics-grid">

      <div className="analytics-card">
        <span>Total Decisions</span>
        <strong>{totalDecisions}</strong>
      </div>

      <div className="analytics-card">
        <span>Successful Decisions</span>
        <strong>{successfulDecisions}</strong>
      </div>

      <div className="analytics-card">
        <span>Success Rate</span>
        <strong>
          {successRate.toFixed(1)}%
        </strong>
      </div>

      <div className="analytics-card">
        <span>Average Predicted Cost</span>
        <strong>
          ${averagePredictedCost.toLocaleString(
            undefined,
            {
              maximumFractionDigits: 0,
            }
          )}
        </strong>
      </div>

    </div>


    {/* DECISION SUMMARY */}

    <div className="analytics-section">

      <h2>Decision Performance</h2>

      <div className="performance-box">

        <div className="performance-row">
          <span>Total Decisions</span>
          <span>{totalDecisions}</span>
        </div>

        <div className="performance-row">
          <span>Successful</span>
          <span>{successfulDecisions}</span>
        </div>

        <div className="performance-row">
          <span>Success Rate</span>
          <span>{successRate.toFixed(1)}%</span>
        </div>

        <div className="performance-row">
          <span>Average Predicted Cost</span>
          <span>
            ${averagePredictedCost.toLocaleString()}
          </span>
        </div>

      </div>

    </div>


    {/* ACTION USAGE */}

    <div className="analytics-section">

      <h2>Actions Used</h2>

      <div className="action-list">

        {actionUsage.length === 0 ? (
          <p>No decisions recorded yet.</p>
        ) : (
          actionUsage.map((item) => (
            <div
              className="action-row"
              key={item.action}
            >

              <div className="action-info">
                <span>{item.action}</span>
                <span>
                  {item.percentage.toFixed(1)}%
                </span>
              </div>

              <div className="action-bar">
                <div
                  className="action-bar-fill"
                  style={{
                    width: `${item.percentage}%`,
                  }}
                />
              </div>

            </div>
          ))
        )}

      </div>

    </div>


    {/* RECENT DECISIONS */}

    <div className="analytics-section">

      <h2>Recent Decisions</h2>

      <div className="decision-table">

        <div className="table-header">
          <span>Shipment</span>
          <span>Action</span>
          <span>Cost</span>
          <span>Status</span>
        </div>

        {decisions.slice(0, 10).map((decision) => (
          <div
            className="table-row"
            key={decision.decision_id}
          >

            <span>
              {decision.shipment_id}
            </span>

            <span>
              {decision.selected_action}
            </span>

            <span>
              ${Number(
                decision.predicted_cost || 0
              ).toLocaleString()}
            </span>

            <span
              className={
                decision.status === "EXECUTED"
                  ? "status-success"
                  : "status-pending"
              }
            >
              {decision.status}
            </span>

          </div>
        ))}

      </div>

    </div>

  </section>
)}
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
    ...recommendations.map((item) => Number(item.cost || 0)),
    1
  );

  const maxDelay = Math.max(
    ...recommendations.map((item) => Number(item.delay || 0)),
    1
  );

  return (
    <div className="cost-speed-chart-new">

      {/* Y AXIS TITLE */}
      <div className="chart-y-title">
        DELIVERY SPEED
      </div>

      {/* CHART */}
      <div className="chart-area-new">

        {/* GRID */}
        <div className="horizontal-line line-1"></div>
        <div className="horizontal-line line-2"></div>
        <div className="horizontal-line line-3"></div>
        <div className="horizontal-line line-4"></div>

        <div className="vertical-line line-1"></div>
        <div className="vertical-line line-2"></div>
        <div className="vertical-line line-3"></div>
        <div className="vertical-line line-4"></div>

        {/* AXES */}
        <div className="x-axis-new"></div>
        <div className="y-axis-new"></div>

        {/* POINTS */}
        {recommendations.map((item, index) => {

          /*
            X POSITION
            Low cost  -> left
            High cost -> right
          */
          const x =
            8 +
            (Number(item.cost || 0) / maxCost) * 82;

          /*
            Y POSITION
            Low delay  -> top
            High delay -> bottom
          */
          const y =
            8 +
            (Number(item.delay || 0) / maxDelay) * 82;

          return (
            <div
              key={item.option}
              className={`chart-point-new point-${index}`}
              style={{
                left: `${Math.min(x, 92)}%`,
                top: `${Math.min(y, 92)}%`,
              }}
            >

              {/* DOT */}
              <div className="point-dot-new"></div>

              {/* LABEL */}
              <div className="point-label-new">
                <strong>{item.option}</strong>

                <span>
                  {formatCurrency(item.cost)}
                </span>

                <span>
                  {item.delay} days
                </span>
              </div>

            </div>
          );
        })}

        {/* AXIS LABELS */}

        <span className="x-label-left">
          <p style={{ fontSize: "10px"}}>
          LOW COST
          </p>
        </span>

        <span className="x-label-right">
          <p style={{ fontSize: "10px"}}>
          HIGH COST
          </p>
        </span>

        <span className="y-label-top">
          <p style={{ fontSize: "10px"}}>
          Fast
          </p>
        </span>

        <span className="y-label-bottom">
          <p style={{ fontSize: "10px"}}>
          Slow
          </p>
        </span>

      </div>
    </div>
  );
}
function OperationalWorkflow({
  selectedShipment,
  selectedRisk,
  recommendations,
  lastExecutedDecision,
  feedbackResult,
  workflowStep,
  setWorkflowStep,
}) {
  const steps = [
    {
      number: 1,
      title: "Alert",
      description: "Shipment risk detected",
      icon: "△",
    },
    {
      number: 2,
      title: "Prediction",
      description: "Analyze expected impact",
      icon: "◉",
    },
    {
      number: 3,
      title: "AI Recommendations",
      description: "Generate recovery options",
      icon: "✦",
    },
    {
      number: 4,
      title: "Compare Options",
      description: "Compare cost and speed",
      icon: "◫",
    },
    {
      number: 5,
      title: "Execute Decision",
      description: "Select an action",
      icon: "→",
    },
    {
      number: 6,
      title: "Confirmation",
      description: "Decision recorded",
      icon: "✓",
    },
    {
      number: 7,
      title: "Track Outcome",
      description: "Record actual result",
      icon: "◌",
    },
    {
      number: 8,
      title: "Measure Impact",
      description: "Evaluate performance",
      icon: "▥",
    },
  ];

  return (
    <section className="workflow-panel panel">
      <div className="panel-header">
        <div>
          <span className="eyebrow">OPERATIONAL WORKFLOW</span>

          <h3>Decision Lifecycle</h3>

          <p>
            Move from shipment alert to measurable business outcome.
          </p>
        </div>

        <div className="workflow-status">
          STEP {workflowStep} / {steps.length}
        </div>
      </div>

      <div className="workflow-container">
        {steps.map((step, index) => {
          const completed = workflowStep > step.number;
          const active = workflowStep === step.number;

          return (
            <div
              key={step.number}
              className={`workflow-step ${
                active ? "active" : ""
              } ${completed ? "completed" : ""}`}
            >
              <div className="workflow-node">
                {completed ? "✓" : step.icon}
              </div>

              <div className="workflow-content">
                <strong>
                  {step.number}. {step.title}
                </strong>

                <span>{step.description}</span>
              </div>

              {index < steps.length - 1 && (
                <div
                  className={`workflow-connector ${
                    completed ? "completed" : ""
                  }`}
                />
              )}
            </div>
          );
        })}
      </div>

      <div className="workflow-context">
        <div>
          <span>SHIPMENT</span>
          <strong>
            {selectedShipment?.shipment_id || "—"}
          </strong>
        </div>

        <div>
          <span>RISK</span>
          <strong className={getRiskClass(selectedRisk)}>
            {selectedRisk}
          </strong>
        </div>

        <div>
          <span>OPTIONS</span>
          <strong>{recommendations.length}</strong>
        </div>

        <div>
          <span>STATUS</span>
          <strong>
            {feedbackResult
              ? "OUTCOME RECORDED"
              : lastExecutedDecision
              ? "DECISION EXECUTED"
              : "AWAITING DECISION"}
          </strong>
        </div>
      </div>
    </section>
  );
}
export default App;