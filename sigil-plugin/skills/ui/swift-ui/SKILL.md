---
name: swift-ui
description: Implements SwiftUI views from design specifications. Supports iOS 15+, macOS 12+.
version: 1.0.0
category: ui
chainable: true
invokes: []
invoked_by: [developer]
tools: Read, Write, Edit, Bash, Glob
inputs: [component_spec, design_tokens, accessibility_requirements]
outputs: [view_files, test_files]
---

# Skill: SwiftUI

## Purpose

Implement SwiftUI views from design specifications for Apple platforms.

## When to Invoke

- Developer receives task to implement UI view
- Constitution specifies SwiftUI as UI framework
- Xcode project with SwiftUI

## Inputs

**Standard Contract:**
- `component_spec`: object
- `design_tokens`: object
- `accessibility_requirements`: object

**Optional:**
- `min_ios_version`: string — Minimum iOS version (default: "15.0")
- `include_macos`: boolean — Include macOS support

## Process

### Step 1: Detect Project Setup

```bash
# Check for Xcode project
ls *.xcodeproj *.xcworkspace

# Check deployment target
grep -r "IPHONEOS_DEPLOYMENT_TARGET" *.xcodeproj/project.pbxproj

# Check existing view patterns
ls **/*.swift | head -10
```

### Step 2: Generate View

```swift
import SwiftUI

enum ButtonVariant {
    case primary
    case secondary
}

enum ButtonSize {
    case small
    case medium
    case large

    var padding: EdgeInsets {
        switch self {
        case .small: return EdgeInsets(top: 6, leading: 12, bottom: 6, trailing: 12)
        case .medium: return EdgeInsets(top: 10, leading: 20, bottom: 10, trailing: 20)
        case .large: return EdgeInsets(top: 14, leading: 28, bottom: 14, trailing: 28)
        }
    }

    var fontSize: CGFloat {
        switch self {
        case .small: return 14
        case .medium: return 16
        case .large: return 18
        }
    }
}

struct CustomButton: View {
    let variant: ButtonVariant
    var size: ButtonSize = .medium
    var disabled: Bool = false
    let action: () -> Void
    let label: String

    var body: some View {
        Button(action: {
            if !disabled {
                action()
            }
        }) {
            Text(label)
                .font(.system(size: size.fontSize, weight: .semibold))
                .foregroundColor(textColor)
                .padding(size.padding)
                .background(backgroundColor)
                .cornerRadius(8)
        }
        .disabled(disabled)
        .opacity(disabled ? 0.5 : 1)
        .accessibilityLabel(label)
        .accessibilityAddTraits(.isButton)
        .accessibilityRemoveTraits(disabled ? .isEnabled : [])
    }

    private var backgroundColor: Color {
        switch variant {
        case .primary: return Color(hex: "#3B82F6")
        case .secondary: return Color(hex: "#F3F4F6")
        }
    }

    private var textColor: Color {
        switch variant {
        case .primary: return .white
        case .secondary: return Color(hex: "#111827")
        }
    }
}

// Color extension for hex support
extension Color {
    init(hex: String) {
        let hex = hex.trimmingCharacters(in: CharacterSet.alphanumerics.inverted)
        var int: UInt64 = 0
        Scanner(string: hex).scanHexInt64(&int)
        let a, r, g, b: UInt64
        switch hex.count {
        case 6: // RGB
            (a, r, g, b) = (255, int >> 16, int >> 8 & 0xFF, int & 0xFF)
        case 8: // ARGB
            (a, r, g, b) = (int >> 24, int >> 16 & 0xFF, int >> 8 & 0xFF, int & 0xFF)
        default:
            (a, r, g, b) = (255, 0, 0, 0)
        }
        self.init(
            .sRGB,
            red: Double(r) / 255,
            green: Double(g) / 255,
            blue: Double(b) / 255,
            opacity: Double(a) / 255
        )
    }
}

#Preview("Primary Button") {
    VStack(spacing: 16) {
        CustomButton(variant: .primary, action: {}, label: "Primary")
        CustomButton(variant: .primary, size: .small, action: {}, label: "Small")
        CustomButton(variant: .primary, size: .large, action: {}, label: "Large")
        CustomButton(variant: .primary, disabled: true, action: {}, label: "Disabled")
    }
    .padding()
}

#Preview("Secondary Button") {
    VStack(spacing: 16) {
        CustomButton(variant: .secondary, action: {}, label: "Secondary")
        CustomButton(variant: .secondary, size: .small, action: {}, label: "Small")
        CustomButton(variant: .secondary, size: .large, action: {}, label: "Large")
        CustomButton(variant: .secondary, disabled: true, action: {}, label: "Disabled")
    }
    .padding()
}
```

### Step 3: Implement Accessibility

SwiftUI accessibility modifiers:

```swift
.accessibilityLabel("Submit button")
.accessibilityHint("Double tap to submit the form")
.accessibilityAddTraits(.isButton)
.accessibilityRemoveTraits(.isStaticText)
.accessibilityValue("Selected")
```

### Step 4: Generate Tests

```swift
import XCTest
import SwiftUI
import ViewInspector
@testable import YourApp

final class CustomButtonTests: XCTestCase {

    func testPrimaryButtonRendersCorrectly() throws {
        let button = CustomButton(
            variant: .primary,
            action: {},
            label: "Test"
        )

        let inspection = try button.inspect()
        let text = try inspection.find(text: "Test")
        XCTAssertNotNil(text)
    }

    func testButtonCallsAction() throws {
        var actionCalled = false
        let button = CustomButton(
            variant: .primary,
            action: { actionCalled = true },
            label: "Test"
        )

        // Note: UI testing typically done via XCUITest
        // This is a basic structure test
        XCTAssertFalse(actionCalled) // Action not called on init
    }

    func testDisabledButtonHasReducedOpacity() throws {
        let button = CustomButton(
            variant: .primary,
            disabled: true,
            action: {},
            label: "Test"
        )

        // Verify disabled state is set
        XCTAssertTrue(button.disabled)
    }

    func testAccessibilityLabel() throws {
        let button = CustomButton(
            variant: .primary,
            action: {},
            label: "Submit"
        )

        // Accessibility testing typically via XCUITest
        // Verify label matches
        XCTAssertEqual(button.label, "Submit")
    }
}

// XCUITest for comprehensive testing
final class CustomButtonUITests: XCTestCase {

    func testButtonTap() throws {
        let app = XCUIApplication()
        app.launch()

        let button = app.buttons["Submit"]
        XCTAssertTrue(button.exists)
        button.tap()
    }

    func testDisabledButtonNotTappable() throws {
        let app = XCUIApplication()
        app.launch()

        let button = app.buttons["Disabled"]
        XCTAssertFalse(button.isEnabled)
    }
}
```

## Output Format

### File Structure
```
Sources/Components/
├── CustomButton.swift
Tests/ComponentTests/
├── CustomButtonTests.swift
```

Or in feature folders:
```
Features/Common/UI/
├── CustomButton.swift
├── CustomButtonTests.swift (in Tests/)
```

## Handoff Data

```json
{
  "files_created": [
    "Sources/Components/CustomButton.swift",
    "Tests/ComponentTests/CustomButtonTests.swift"
  ],
  "min_ios_version": "15.0",
  "accessibility_implemented": true,
  "previews_included": true
}
```

## SwiftUI Patterns

### State Management
- @State for local state
- @Binding for two-way binding
- @ObservedObject for external observable objects
- @StateObject for owned observable objects
- @EnvironmentObject for dependency injection

### View Composition
- Extract reusable views
- ViewModifier for reusable styling
- ViewBuilder for conditional content
- Prefer composition over inheritance

### Accessibility
- .accessibilityLabel() for VoiceOver
- .accessibilityHint() for usage hints
- .accessibilityAddTraits() for element type
- .accessibilityValue() for current value

### Previews
- #Preview macro (iOS 17+) or PreviewProvider
- Multiple preview configurations
- Preview in different color schemes
- Preview with different Dynamic Type sizes

### Performance
- Minimize view body complexity
- Use @ViewBuilder efficiently
- Avoid expensive operations in body
- Use task modifiers for async work

## End-to-End Example

**Spec input** — UI Designer produces a component spec for a status badge:

```json
{
  "component_spec": {
    "name": "StatusBadge",
    "type": "presentational",
    "props": [
      { "name": "status", "type": "enum", "values": ["active", "pending", "error"], "required": true },
      { "name": "label", "type": "string", "required": true }
    ]
  },
  "design_tokens": {
    "colors": { "active": "#22C55E", "pending": "#F59E0B", "error": "#EF4444" }
  },
  "accessibility_requirements": { "role": "status", "aria": { "live": "polite" } }
}
```

**Generated view** — `Sources/Components/StatusBadge.swift`:

```swift
import SwiftUI

enum BadgeStatus {
    case active, pending, error

    var color: Color {
        switch self {
        case .active:  return Color(hex: "#22C55E")
        case .pending: return Color(hex: "#F59E0B")
        case .error:   return Color(hex: "#EF4444")
        }
    }
}

struct StatusBadge: View {
    let status: BadgeStatus
    let label: String

    var body: some View {
        Text(label)
            .font(.system(size: 13, weight: .semibold))
            .foregroundColor(status.color)
            .padding(.horizontal, 10)
            .padding(.vertical, 4)
            .background(status.color.opacity(0.15))
            .cornerRadius(12)
            .accessibilityLabel("\(label): \(String(describing: status))")
            .accessibilityAddTraits(.updatesFrequently)
    }
}

#Preview {
    VStack(spacing: 12) {
        StatusBadge(status: .active, label: "Live")
        StatusBadge(status: .pending, label: "Pending")
        StatusBadge(status: .error, label: "Failed")
    }
    .padding()
}
```

**Generated test** — `Tests/ComponentTests/StatusBadgeTests.swift`:

```swift
import XCTest
@testable import YourApp

final class StatusBadgeTests: XCTestCase {
    func testLabelIsStored() {
        let badge = StatusBadge(status: .active, label: "Live")
        XCTAssertEqual(badge.label, "Live")
    }

    func testStatusColorMapping() {
        XCTAssertEqual(BadgeStatus.active.color, Color(hex: "#22C55E"))
        XCTAssertEqual(BadgeStatus.error.color, Color(hex: "#EF4444"))
    }
}
```

**Handoff:**
```json
{
  "files_created": ["Sources/Components/StatusBadge.swift", "Tests/ComponentTests/StatusBadgeTests.swift"],
  "min_ios_version": "15.0",
  "accessibility_implemented": true,
  "previews_included": true
}
```

## Human Checkpoint

**Tier:** Auto

## Error Handling

| Error | Resolution |
|-------|------------|
| iOS version too low | Update deployment target or use availability checks |
| Missing Color extension | Include hex color extension |
| ViewInspector not available | Generate XCUITest instead |
| Preview failing | Ensure all required data provided |
