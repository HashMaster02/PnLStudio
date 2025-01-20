export function MetricCards({ data }) {
    return (
        <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-5 gap-4 mb-4 ">
            <div className="rounded-xl border border-gray-200 p-4">
                <div className="text-sm text-gray-600">Total Gains (C1)</div>
                <div className="text-2xl font-semibold mt-1">
                    {data && data.total_gains
                        ? `$${Math.trunc(data.total_gains).toLocaleString()}`
                        : 'No Data'}
                </div>
            </div>
            <div className="rounded-xl border border-gray-200 p-4">
                <div className="text-sm text-gray-600">Realized Gains</div>
                <div className="text-2xl font-semibold mt-1">
                    {data && data.realized_gains
                        ? `$${Math.trunc(data.realized_gains).toLocaleString()}`
                        : 'No Data'}
                </div>
            </div>
            <div className="rounded-xl border border-gray-200 p-4">
                <div className="text-sm text-gray-600">Unrealized Gains</div>
                <div className="text-2xl font-semibold mt-1">
                    {data && data.unrealized_gains
                        ? `$${Math.trunc(
                              data.unrealized_gains
                          ).toLocaleString()}`
                        : 'No Data'}
                </div>
            </div>
            <div className="rounded-xl border border-gray-200 p-4">
                <div className="text-sm text-gray-600">Interest</div>
                <div className="text-2xl font-semibold mt-1 ">
                    {data && data.interest
                        ? `$${Math.trunc(data.interest).toLocaleString()}`
                        : 'No Data'}
                </div>
            </div>
            <div className="rounded-xl border border-gray-200 p-4">
                <div className="text-sm text-gray-600">Dividend</div>
                <div className="text-2xl font-semibold mt-1">
                    {data && data.dividends
                        ? `$${Math.trunc(data.dividends).toLocaleString()}`
                        : 'No Data'}
                </div>
            </div>
        </div>
    );
}
