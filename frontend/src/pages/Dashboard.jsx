import { useEffect, useState } from 'react';
import { getProducts, createProduct, deleteProduct, getProductWithPrices } from '../api';
import ProductList from '../components/ProductList';
import ProductForm from '../components/ProductForm';

export default function Dashboard() {
  const [products, setProducts] = useState([]);
  const [loading, setLoading] = useState(true);
  const [showForm, setShowForm] = useState(false);

  const loadProducts = async () => {
    setLoading(true);
    try {
      const res = await getProducts();
      setProducts(res.data);
    } catch (err) {
      console.error(err);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    loadProducts();
  }, []);

  const handleCreate = async (productData) => {
    try {
      await createProduct(productData);
      await loadProducts();
      setShowForm(false);
    } catch (err) {
      alert('Ошибка добавления товара');
    }
  };

  const handleDelete = async (id) => {
    if (window.confirm('Удалить товар?')) {
      await deleteProduct(id);
      await loadProducts();
    }
  };

  const handleViewHistory = async (productId) => {
    try {
      const res = await getProductWithPrices(productId, 30);
      return res.data.prices || [];
    } catch (err) {
      console.error(err);
      return [];
    }
  };

  return (
    <div className="container">
      <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '1.5rem' }}>
        <h1>Мои товары</h1>
        <button className="btn btn-primary" onClick={() => setShowForm(!showForm)}>
          {showForm ? 'Отмена' : '+ Добавить товар'}
        </button>
      </div>

      {showForm && (
        <div className="card" style={{ marginBottom: '2rem' }}>
          <h3>Новый товар</h3>
          <ProductForm onSubmit={handleCreate} />
        </div>
      )}

      <ProductList
        products={products}
        onDelete={handleDelete}
        onViewHistory={handleViewHistory}
        loading={loading}
      />
    </div>
  );
}