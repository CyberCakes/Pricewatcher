import { useState } from 'react';

export default function ProductForm({ onSubmit, initialData = null }) {
  const [url, setUrl] = useState(initialData?.url || '');
  const [name, setName] = useState(initialData?.name || '');
  const [priceSelector, setPriceSelector] = useState(initialData?.price_selector || '');
  const [parseInterval, setParseInterval] = useState(initialData?.parse_interval_minutes || 1440);
  const [notifyDrop, setNotifyDrop] = useState(initialData?.notify_drop_percent || 5);

  const handleSubmit = (e) => {
    e.preventDefault();
    onSubmit({
      url,
      name: name || undefined,
      price_selector: priceSelector || undefined,
      parse_interval_minutes: parseInt(parseInterval, 10),
      notify_drop_percent: parseInt(notifyDrop, 10)
    });
  };

  return (
    <form onSubmit={handleSubmit}>
      <div className="form-group">
        <label>URL товара *</label>
        <input type="url" value={url} onChange={e => setUrl(e.target.value)} required />
      </div>
      <div className="form-group">
        <label>Название (опционально)</label>
        <input type="text" value={name} onChange={e => setName(e.target.value)} />
      </div>
      <div className="form-group">
        <label>CSS-селектор цены (опционально)</label>
        <input type="text" value={priceSelector} onChange={e => setPriceSelector(e.target.value)} placeholder=".price, #cost, [data-price]" />
        <small>Если не указать, будет использован автоматический по домену</small>
      </div>
      <div className="form-group">
        <label>Интервал парсинга (минуты)</label>
        <select value={parseInterval} onChange={e => setParseInterval(e.target.value)}>
          <option value={60}>Каждый час</option>
          <option value={360}>Каждые 6 часов</option>
          <option value={720}>Каждые 12 часов</option>
          <option value={1440}>Раз в день</option>
          <option value={4320}>Раз в 3 дня</option>
        </select>
      </div>
      <div className="form-group">
        <label>Уведомлять при снижении на (%)</label>
        <input type="number" min="1" max="100" value={notifyDrop} onChange={e => setNotifyDrop(e.target.value)} />
      </div>
      <button type="submit" className="btn btn-primary">Сохранить</button>
    </form>
  );
}