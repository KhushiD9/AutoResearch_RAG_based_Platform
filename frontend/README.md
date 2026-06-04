# Frontend - Research Paper Assistant

Angular-based frontend with glassmorphism UI design.

## Features

- Modern glassmorphism design
- Responsive layout
- Paper search interface
- Interactive chat for questions
- Query history viewer
- Multiple query modes
- Real-time updates

## Installation

1. Install dependencies:
```cmd
npm install
```

2. Start development server:
```cmd
npm start
```

Application runs at: http://localhost:4200

## Project Structure

```
frontend/src/
├── app/
│   ├── components/      # UI components
│   ├── services/        # API and state services
│   ├── app.module.ts    # Main module
│   └── app-routing.module.ts
├── styles.scss          # Global styles
└── index.html
```

## Available Scripts

- `npm start` - Start development server
- `npm run build` - Build for production
- `npm run watch` - Build and watch for changes

## Design System

### Glassmorphism

The UI uses a glassmorphism design with:
- Frosted glass effects
- Transparent backgrounds with blur
- Subtle borders and shadows
- Gradient backgrounds

### Color Scheme

- Primary gradient: Purple to violet
- Glass effects: White with transparency
- Text: White with various opacities

### Components

1. **Header** - Navigation bar
2. **Search** - Paper discovery interface
3. **Chat** - Question answering interface
4. **History** - Query history viewer
5. **Loader** - Loading indicator

## Customization

### Change API endpoint:

Edit `src/app/services/api.service.ts`:
```typescript
private baseUrl = 'http://localhost:8000/api';
```

### Modify colors:

Edit `src/styles.scss` gradient and glass effects.

## Browser Support

- Chrome (recommended)
- Firefox
- Safari
- Edge

Note: Glassmorphism effects work best on modern browsers with backdrop-filter support.

## Build for Production

```cmd
npm run build
```

Output will be in `dist/` directory.

Deploy the `dist/research-paper-assistant` folder to your web server.
