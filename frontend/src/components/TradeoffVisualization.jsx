function TradeoffVisualization({ recommendations }) {

    if (!recommendations || recommendations.length === 0) {
        return null;
    }

    const maxCost = Math.max(
        ...recommendations.map((item) => Number(item.cost))
    );

    const maxDelay = Math.max(
        ...recommendations.map((item) => Number(item.expected_delay))
    );

    return (
        <section className="tradeoff-section">

            <div className="section-title">
                <h2>Cost vs Speed</h2>

                <p>
                    Compare the cost and expected delay
                    of each recommendation.
                </p>
            </div>

            <div className="tradeoff-chart">

                <div className="y-axis-label">
                    SPEED
                </div>

                <div className="chart-area">

                    {recommendations.map((item) => {

                        const cost =
                            Number(item.cost);

                        const delay =
                            Number(item.expected_delay);

                        const left =
                            (cost / maxCost) * 85;

                        const top =
                            (delay / maxDelay) * 75;

                        return (
                            <div
                                key={item.recommendation_id}
                                className="tradeoff-point"
                                style={{
                                    left: `${left}%`,
                                    top: `${top}%`,
                                }}
                            >
                                <div className="point-dot"></div>

                                <span>
                                    {item.action}
                                </span>
                            </div>
                        );
                    })}

                    <div className="x-axis">
                        COST →
                    </div>

                </div>
            </div>

        </section>
    );
}

export default TradeoffVisualization;