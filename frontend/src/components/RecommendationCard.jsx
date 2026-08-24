function RecommendationCard({ recommendation, onExecute }) {
    const {
        rank_order,
        action,
        cost,
        expected_delay,
        risk,
        selected_action,
        decision_status,
    } = recommendation;

    const isSelected =
        selected_action === action ||
        decision_status === "SELECTED";

    const riskClass = risk?.toLowerCase() || "low";

    return (
        <div
            className={`recommendation-card ${
                isSelected ? "selected-card" : ""
            }`}
        >
            <div className="recommendation-header">
                <div>
                    <span className="option-label">
                        OPTION {rank_order}
                    </span>

                    <h3>{action}</h3>
                </div>

                {isSelected && (
                    <span className="selected-badge">
                        SELECTED
                    </span>
                )}
            </div>

            <div className="recommendation-details">

                <div className="detail-item">
                    <span>Cost</span>
                    <strong>
                        ₹{Number(cost).toLocaleString("en-IN")}
                    </strong>
                </div>

                <div className="detail-item">
                    <span>Expected Delay</span>
                    <strong>
                        {expected_delay} days
                    </strong>
                </div>

                <div className="detail-item">
                    <span>Risk</span>

                    <strong className={`risk ${riskClass}`}>
                        {risk}
                    </strong>
                </div>

            </div>

            <button
                className="execute-button"
                onClick={() => onExecute(recommendation)}
            >
                Execute Decision
            </button>
        </div>
    );
}

export default RecommendationCard;