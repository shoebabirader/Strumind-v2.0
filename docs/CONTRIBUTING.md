# Contributing to StruMind

Thank you for your interest in contributing to StruMind!

## Development Setup

1. Fork the repository
2. Clone your fork
3. Create a feature branch
4. Make your changes
5. Submit a pull request

## Code Standards

### Python (Backend)
- Follow PEP 8 style guide
- Use type hints
- Write docstrings for all functions
- Maximum line length: 100 characters

```python
def calculate_moment(force: float, distance: float) -> float:
    """Calculate bending moment.
    
    Args:
        force: Applied force in N
        distance: Distance from support in m
    
    Returns:
        Bending moment in Nm
    """
    return force * distance
```

### TypeScript (Frontend)
- Use TypeScript strict mode
- Follow Airbnb style guide
- Use functional components with hooks
- Proper prop typing

```typescript
interface ButtonProps {
  label: string
  onClick: () => void
  disabled?: boolean
}

export const Button: React.FC<ButtonProps> = ({ label, onClick, disabled = false }) => {
  return <button onClick={onClick} disabled={disabled}>{label}</button>
}
```

## Testing

### Backend Tests
```bash
cd backend
pytest tests/ --cov=app --cov-report=html
```

### Frontend Tests
```bash
cd frontend
npm test
```

## Commit Messages

Follow conventional commits:
- `feat:` New feature
- `fix:` Bug fix
- `docs:` Documentation
- `style:` Formatting
- `refactor:` Code restructuring
- `test:` Adding tests
- `chore:` Maintenance

Example:
```
feat: add pushover analysis support

- Implement pushover curve generation
- Add capacity spectrum method
- Update API endpoints
```

## Pull Request Process

1. Update documentation
2. Add tests for new features
3. Ensure all tests pass
4. Update CHANGELOG.md
5. Request review from maintainers

## Areas for Contribution

### High Priority
- Additional design codes (Eurocode, BS)
- Advanced analysis methods (P-Delta, buckling)
- Performance optimization
- UI/UX improvements

### ML/AI Enhancements
- Improve model accuracy
- Add more training data
- Implement transfer learning
- Optimize inference speed

### BIM Integration
- Support for more file formats
- Enhanced visualization
- Clash detection
- Quantity takeoff automation

### Documentation
- API documentation
- User guides
- Video tutorials
- Code examples

## Questions?

Open an issue or contact the maintainers.
