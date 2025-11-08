# Black Friday Sale Tracker Dashboard

Modern, responsive web dashboard for monitoring Black Friday sales across multiple retailers.

## Features

### 1. Real-Time Statistics
- **Total Products**: Count of all monitored products
- **Items On Sale**: Current sale count with percentage
- **Average Discount**: Average discount across all sales
- **Total Savings**: Cumulative potential savings

### 2. Product Filtering
- **All Products**: View entire product catalog
- **On Sale Only**: Filter to show only discounted items
- **Regular Price**: View products at regular price

### 3. Flexible Sorting
- Discount % (High to Low)
- Discount % (Low to High)
- Price (Low to High)
- Price (High to Low)
- Recently Checked

### 4. Auto-Refresh System
- Automatic data refresh every 5 minutes
- Live countdown timer showing next refresh
- Manual refresh button for instant updates
- Spinning indicator during data loading

### 5. Product Cards
Each product card displays:
- Product name and retailer
- Current price (large, prominent)
- Original price (strikethrough if on sale)
- Sale badge with discount percentage
- Savings amount
- "View Product" button
- Last checked timestamp

### 6. Responsive Design
- Desktop: 3-4 cards per row
- Tablet: 2-3 cards per row
- Mobile: 1 card per row (full width)
- Adaptive header and controls

### 7. User Experience
- **Filter Persistence**: Remembers your filter selection
- **Sort Persistence**: Remembers your sort preference
- **Smooth Animations**: Fade-in effects on data updates
- **Loading States**: Spinner and loading messages
- **Empty States**: Context-aware messages for no results
- **Error Handling**: User-friendly error messages
- **Accessibility**: ARIA labels, keyboard navigation, screen reader support

## Design

### Color Scheme
- **Primary Red**: `#DC2626` - Buttons, sale highlights
- **Secondary Dark**: `#1F2937` - Text, headers
- **Accent Gold**: `#F59E0B` - Discount badges
- **Background**: `#F9FAFB` - Light gray page background
- **On Sale Background**: `#FEE2E2` - Light red card background
- **Success Green**: `#10B981` - Prices, savings

### Typography
- System font stack for native feel
- Responsive font sizes (clamp for fluid scaling)
- Clear hierarchy with font weights

### Layout
- Maximum width: 1400px (centered)
- Flexible grid system (CSS Grid)
- Card-based design with shadows and hover effects

## Technical Details

### Architecture
- **Single HTML File**: No build process required
- **Vanilla JavaScript**: No external frameworks
- **Pure CSS**: No CSS frameworks
- **Flask Backend**: REST API integration

### API Endpoints Used
```
GET /api/stats           - Summary statistics
GET /api/products        - All products with status
GET /api/products/:id/history - Price history (not currently used)
GET /api/sales/recent    - Recent sales (not currently used)
GET /api/products/on-sale - On sale products (not currently used)
```

### Browser Compatibility
- Chrome 90+
- Firefox 88+
- Safari 14+
- Edge 90+

### Performance
- Fast initial load (< 2 seconds)
- Client-side filtering and sorting (instant)
- Efficient DOM updates
- Debounced API calls

### State Management
```javascript
allProducts = []          // Cached product data
currentFilter = 'all'     // Active filter (localStorage)
currentSort = 'discount-high' // Active sort (localStorage)
refreshTimer = null       // Auto-refresh interval
countdownTimer = null     // Countdown update interval
isLoading = false        // Request throttling
```

### Key Functions
```javascript
loadData()              // Fetch stats and products
displayProducts()       // Render filtered/sorted products
filterProducts()        // Apply current filter
sortProducts()          // Apply current sort
createProductCard()     // Generate product HTML
startRefreshTimer()     // Initialize auto-refresh
formatCurrency()        // Format prices
getTimeAgo()           // Format timestamps
extractRetailer()      // Parse domain from URL
```

## Usage

### Starting the Dashboard

1. **Install Dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

2. **Start Flask Server**:
   ```bash
   python app.py
   ```

3. **Open Dashboard**:
   ```
   http://localhost:5000/
   ```

### Configuration

**Change Refresh Interval** (in dashboard.html):
```javascript
const REFRESH_INTERVAL = 5 * 60 * 1000; // 5 minutes (in milliseconds)
```

**Change API Base URL** (for production):
```javascript
const API_BASE = 'https://your-domain.com'; // Default: window.location.origin
```

## Customization

### Colors
Edit CSS variables in `:root`:
```css
:root {
    --primary: #DC2626;      /* Red */
    --secondary: #1F2937;    /* Dark gray */
    --accent: #F59E0B;       /* Gold */
    --background: #F9FAFB;   /* Light gray */
    --on-sale-bg: #FEE2E2;   /* Light red */
    --success: #10B981;      /* Green */
}
```

### Layout
Adjust grid columns:
```css
.products-grid {
    grid-template-columns: repeat(auto-fill, minmax(300px, 1fr));
    /* Change 300px to adjust card minimum width */
}
```

### Card Content
Modify `createProductCard()` function to add/remove fields:
```javascript
function createProductCard(product) {
    // Customize HTML structure here
}
```

## Accessibility

### ARIA Support
- `role="tablist"` on filter tabs
- `role="tab"` on each filter button
- `aria-selected` states for active filters
- `aria-label` on interactive elements
- `role="region"` on product container
- `aria-live="polite"` for dynamic content

### Keyboard Navigation
- Tab through all interactive elements
- Focus visible outlines (2px red)
- Enter/Space to activate buttons
- Escape to close (future modals)

### Screen Readers
- Semantic HTML (`header`, `footer`, `nav`)
- Alt text for loading spinner
- Live region announcements for updates
- Descriptive button labels

### Reduced Motion
Respects `prefers-reduced-motion` media query:
```css
@media (prefers-reduced-motion: reduce) {
    *, *::before, *::after {
        animation-duration: 0.01ms !important;
        transition-duration: 0.01ms !important;
    }
}
```

## Error Handling

### API Errors
- Connection failures show error container
- Failed requests display user-friendly message
- Console logging for debugging

### Data Errors
- Missing prices show "N/A"
- Invalid dates show "Unknown"
- Malformed URLs handled gracefully

### Edge Cases
- Empty product list shows empty state
- No sales shows "No Sales Yet" message
- All on sale shows "All On Sale!" message

## Future Enhancements

### Potential Features
1. **Price History Charts**: Line charts showing price trends
2. **Email Alerts**: Notify on new sales
3. **Wishlist**: Save favorite products
4. **Price Alerts**: Custom price thresholds
5. **Compare Products**: Side-by-side comparison
6. **Search**: Filter by product name or retailer
7. **Categories**: Group by product type
8. **Export**: Download CSV of products
9. **Dark Mode**: Toggle theme
10. **PWA**: Install as mobile app

### Technical Improvements
1. **Service Worker**: Offline support
2. **IndexedDB**: Local caching
3. **WebSocket**: Real-time updates
4. **Lazy Loading**: Virtual scrolling for 1000+ products
5. **Image Optimization**: WebP with fallbacks
6. **Bundle Analysis**: Performance optimization

## Deployment

### Development
```bash
python app.py
# Dashboard: http://localhost:5000/
```

### Production (with Gunicorn)
```bash
pip install gunicorn
gunicorn -w 4 -b 0.0.0.0:8000 app:app
# Dashboard: http://your-server:8000/
```

### Docker
```dockerfile
FROM python:3.11-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . .
EXPOSE 5000
CMD ["python", "app.py"]
```

### Environment Variables
```bash
PORT=5000              # Server port
DEBUG=False            # Debug mode (True/False)
FLASK_ENV=production   # Flask environment
```

## Troubleshooting

### Dashboard Not Loading
1. Check Flask server is running: `curl http://localhost:5000/api/health`
2. Check browser console for errors (F12)
3. Verify database file exists: `ls data/products.db`

### No Products Showing
1. Check API response: `curl http://localhost:5000/api/products`
2. Run initial data load: `python init_products.py`
3. Check database: `sqlite3 data/products.db "SELECT COUNT(*) FROM products;"`

### Styles Not Applying
1. Clear browser cache (Ctrl+Shift+R)
2. Check CSS in dashboard.html is intact
3. Verify no ad blockers interfering

### Auto-Refresh Not Working
1. Check browser console for errors
2. Verify JavaScript not blocked
3. Check `REFRESH_INTERVAL` constant

## License

Part of Black Friday Sale Tracker system.

## Support

For issues or questions, see main project README.md
