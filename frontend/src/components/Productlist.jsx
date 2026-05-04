import { useState } from 'react';
import PriceChart from './PriceChart';

export default function ProductList({ products, onDelete, onViewHistory, loading }) {
  const [expandedProductId, setExpandedProductId] = useState(null);
  const [priceHistory, setPriceHistory] = useState({});

  const handleExpand = async (productId) => {
    if (expandedProductId === productId) {
      setExpandedProductId(null);
      return;
    }
    setExpandedProductId(productId);
    // Загружаем историю цен
    const history = await onViewHistory(productId);
    setPriceHistory(prev => ({ ...prev, [productId]: history }));
  };

  if (loading) return <div>Загрузка...</div>;
  if (!products.length) return <div>У вас пока нет товаров. Добавьте первый!</div>;

  return (
    <div>
      {products.map(product => (
        <div key={product.id} className="card" style={{ marginBottom: '1rem' }}>
          <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'start' }}>
            <div style={{ flex: 1 }}>
              <h3>{product.name || product.url}</h3>
              <p><a href={product.url} target="_blank" rel="noopener noreferrer">{product.url}</a></p>
              <small>Последний парсинг: {product.last_parsed_at ? new Date(product.last_parsed_at).toLocaleString() : 'никогда'}</small>
              <br />
              <small>Интервал: {product.parse_interval_minutes} мин.</small>
            </div>
            <div style={{ display: 'flex', gap: '0.5rem' }}>
              <button className="btn" onClick={() => handleExpand(product.id)}>
                {expandedProductId === product.id ? 'Скрыть график' : 'Показать график'}
              </button>
              <button className="btn btn-danger" onClick={() => onDelete(product.id)}>Удалить</button>
            </div>
          </div>
          {expandedProductId === product.id && (
            <div style={{ marginTop: '1rem' }}>
              {priceHistory[product.id]?.length > 0 ? (
                <PriceChart data={priceHistory[product.id]} />
              ) : (
                <div>Нет истории цен. Дождитесь первого парсинга.</div>
              )}
            </div>
          )}
        </div>
      ))}
    </div>
  );
}