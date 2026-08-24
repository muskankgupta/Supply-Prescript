function ComparisonTable({ recommendations }) {

    return (
        <section className="comparison-section">

            <div className="section-title">
                <h2>Recommendation Comparison</h2>

                <p>
                    Compare all available options before
                    making an operational decision.
                </p>
            </div>

            <div className="table-container">

                <table>

                    <thead>
                        <tr>
                            <th>Option</th>
                            <th>Cost</th>
                            <th>Expected Delay</th>
                            <th>Risk</th>
                        </tr>
                    </thead>

                    <tbody>

                        {recommendations.map((item) => (

                            <tr key={item.recommendation_id}>

                                <td>
                                    <strong>
                                        {item.action}
                                    </strong>
                                </td>

                                <td>
                                    ₹
                                    {Number(
                                        item.cost
                                    ).toLocaleString("en-IN")}
                                </td>

                                <td>
                                    {item.expected_delay} days
                                </td>

                                <td>
                                    <span
                                        className={`risk-badge ${item.risk?.toLowerCase()}`}
                                    >
                                        {item.risk}
                                    </span>
                                </td>

                            </tr>

                        ))}

                    </tbody>

                </table>

            </div>

        </section>
    );
}

export default ComparisonTable;