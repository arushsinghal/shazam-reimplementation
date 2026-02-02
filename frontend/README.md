# Frontend - Shazam Clone

Modern Next.js frontend for the Shazam Clone application.

## Structure

```
frontend/
├── pages/
│   ├── _app.tsx           # App wrapper
│   ├── _document.tsx      # Document wrapper
│   ├── index.tsx          # Home page
│   ├── add-songs.tsx      # Add songs interface
│   └── recognize.tsx      # Recognition interface
├── lib/
│   └── api.ts             # API client (axios)
├── styles/
│   └── globals.css        # Global styles
├── package.json           # Dependencies
└── tsconfig.json          # TypeScript config
```

## Installation

```bash
cd frontend
npm install
```

## Running

### Development
```bash
npm run dev
```

Server runs on `http://localhost:3000`

### Production
```bash
npm run build
npm start
```

## Environment

Create `.env.local`:

```env
NEXT_PUBLIC_API_URL=http://localhost:8000
```

For production:
```env
NEXT_PUBLIC_API_URL=https://your-api-domain.com
```

## Features

### Home Page (`/`)
- Gradient hero section
- Two primary action cards
- Feature highlights
- Responsive design

### Add Songs Page (`/add-songs`)
- File upload (drag-and-drop)
- Song name input
- Processing state
- Success/error feedback

### Recognize Page (`/recognize`)
- Audio clip upload
- Animated "Listening..." state
- Result display:
  - Song name
  - Position in song
  - Confidence level
  - Match score
- Try again flow

## Styling

- **Framework:** Tailwind CSS
- **Icons:** Lucide React
- **Animations:** CSS + Tailwind
- **Responsive:** Mobile-first design

## API Integration

Uses axios for HTTP requests. See `lib/api.ts`:

```typescript
import { api } from '@/lib/api';

// Add song
const result = await api.addSong(songName, file);

// Recognize
const result = await api.recognizeSong(file);

// List songs
const list = await api.listSongs();
```

## Building

```bash
npm run build
```

Output in `.next/` directory.

## Deployment

### Vercel (Recommended)
```bash
vercel deploy --prod
```

### Docker
```dockerfile
FROM node:18-alpine
WORKDIR /app
COPY package*.json ./
RUN npm ci
COPY . .
RUN npm run build
CMD ["npm", "start"]
```

### Static Export (Not supported - uses API routes)

## Performance

- Fast page loads with Next.js optimization
- Image optimization (if images added)
- Code splitting
- CSS purging with Tailwind

## Browser Support

- Chrome/Edge: Latest 2 versions
- Firefox: Latest 2 versions
- Safari: Latest 2 versions
- Mobile: iOS Safari, Chrome Android

## Development Tips

### Hot Reload
Changes auto-reload during `npm run dev`

### Type Checking
```bash
npx tsc --noEmit
```

### Linting
```bash
npm run lint
```

### Clean Install
```bash
rm -rf node_modules .next
npm install
```

## Troubleshooting

**API connection errors:**
- Verify backend is running
- Check `.env.local` has correct API URL
- Check browser console for CORS errors

**Build errors:**
```bash
rm -rf .next
npm run build
```

**Type errors:**
```bash
npm install --save-dev @types/node @types/react @types/react-dom
```

## Customization

### Colors
Edit `tailwind.config.js`:
```javascript
colors: {
  primary: {
    DEFAULT: '#3B82F6',  // Change these
    dark: '#2563EB',
    light: '#60A5FA',
  }
}
```

### Layout
Edit `pages/_app.tsx` to add global layout

### Fonts
Add to `pages/_document.tsx`:
```tsx
<link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap" rel="stylesheet" />
```

## Testing

```bash
# Install testing libraries
npm install --save-dev @testing-library/react @testing-library/jest-dom jest

# Run tests
npm test
```

## Future Enhancements

- [ ] Dark mode toggle
- [ ] Microphone recording
- [ ] Real-time recognition
- [ ] Audio visualization
- [ ] History/favorites
- [ ] Share results

## Dependencies

- `next` - React framework
- `react` - UI library
- `typescript` - Type safety
- `tailwindcss` - Styling
- `axios` - HTTP client
- `lucide-react` - Icons
