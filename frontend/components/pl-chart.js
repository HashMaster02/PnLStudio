import {
    CartesianGrid,
    Line,
    LineChart,
    ResponsiveContainer,
    Tooltip,
    XAxis,
    YAxis,
} from 'recharts';
import PLTabs from './pl-tab-select';

const formatData = (dates, values) => {
    return dates.map((date, index) => ({
        date,
        value: Math.trunc(values[index]),
    }));
};

const CustomTooltip = ({ active, payload, label }) => {
    if (active && payload && payload.length) {
        return (
            <div className="bg-blue-300 bg-opacity-50 px-4 py-2 rounded-md">
                <p className="font-semibold">{`Date: ${label}`}</p>
                <p>{`Value: $${payload[0].value.toLocaleString()}`}</p>
            </div>
        );
    }

    return null;
};

export function PLChart({ pnltype, onChange, data }) {
    return (
        <div className="lg:col-span-2 rounded-xl border border-gray-200 p-4 space-y-6">
            {data ? (
                <>
                    <PLTabs selected={pnltype} onChange={onChange} />
                    <ResponsiveContainer aspect={2}>
                        <LineChart data={formatData(data.date, data.value)}>
                            <CartesianGrid />
                            <XAxis
                                dataKey="date"
                                style={{ fontSize: '12px' }}
                                tickFormatter={(date) =>
                                    `${date.split('-')[1]}/${
                                        date.split('-')[2]
                                    }`
                                }
                                allowDuplicatedCategory={false}
                            />
                            <YAxis
                                dataKey="value"
                                tickFormatter={(value) =>
                                    `${(value / 1000000).toFixed(2)}M`
                                }
                                style={{ fontSize: '12px' }}
                            />
                            <Tooltip content={<CustomTooltip />} />
                            <Line
                                type="monotone"
                                dataKey="value"
                                stroke="#8884d8"
                                dot={false}
                            />
                        </LineChart>
                    </ResponsiveContainer>
                </>
            ) : (
                <h1 className="font-bold text-center">No Data</h1>
            )}
        </div>
    );
}
