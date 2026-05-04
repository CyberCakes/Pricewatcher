import { LineChart, Line, XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer } from 'recharts';
import { format } from 'date-fns';
import { ru } from 'date-fns/locale';

export default function PriceChart({ data }) {
  if (!data || data.length === 0) {
    return <div>Нет данных для отображения графика</div>;
  }

  // Преобразуем данные для recharts
  const chartData = data.map(item => ({
    date: format(new Date(item.timestamp), 'dd.MM', { locale: ru }),
    price: Number(item.price),
    fullDate: item.timestamp
  }));

  return (
    <ResponsiveContainer width="100%" height={300}>
      <LineChart data={chartData}>
        <CartesianGrid strokeDasharray="3 3" />
        <XAxis dataKey="date" />
        <YAxis domain={['auto', 'auto']} />
        <Tooltip
          labelFormatter={(label, payload) => {
            if (payload && payload[0]) {
              return format(new Date(payload[0].payload.fullDate), 'dd.MM.yyyy HH:mm', { locale: ru });
            }
            return label;
          }}
          formatter={(value) => [`${value} ₽`, 'Цена']}
        />
        <Line type="monotone" dataKey="price" stroke="#3b82f6" strokeWidth={2} dot={{ r: 4 }} />
      </LineChart>
    </ResponsiveContainer>
  );
}