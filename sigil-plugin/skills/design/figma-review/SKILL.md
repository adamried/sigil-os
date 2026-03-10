---
name: figma-review
description: Extracts design specifications from Figma. Invoke when user says "I have a Figma file", "here's the design", "check the Figma", shares a figma.com URL, or references Figma designs/mockups/wireframes. Also triggers when uiux-designer needs design source of truth before component design.
version: 1.0.0
category: design
chainable: true
invokes: []
invoked_by: [uiux-designer]
tools: Read, Write, ToolSearch, mcp__figma__get_design_context, mcp__figma__get_screenshot, mcp__figma__get_metadata, mcp__figma__get_variable_defs
inputs: [figma_file_url, figma_node_ids]
outputs: [design_tokens, component_specs, layout_specs]
---

# Skill: Figma Review

## Purpose

Extract design specifications from Figma designs via MCP connection. This skill bridges design tools with implementation by capturing tokens, component specs, and layout details in a format developers can use.

## Prerequisites

- Figma MCP must be connected in Claude settings
- User must have access to the Figma file
- File URL or specific node IDs needed

## When to Invoke

- User indicates they have Figma designs
- Before component design when Figma assets exist
- To validate implementation against designs
- UI/UX Designer needs design source of truth

## Inputs

**Required (one of):**
- `figma_file_url`: string — URL to Figma file
- `figma_node_ids`: string[] — Specific node IDs to extract

**Optional:**
- `extract_tokens`: boolean — Extract design tokens (default: true)
- `extract_components`: boolean — Extract component specs (default: true)
- `extract_layout`: boolean — Extract layout/spacing (default: true)

## Process

### Step 1: Verify MCP Connection

Check for Figma MCP availability:

```
If Figma MCP not available:
  → Return error with connection instructions
  → Offer to proceed without Figma
```

### Step 2: Access Figma File

Using Figma MCP tools:
1. Parse file URL to extract file key
2. Request file metadata
3. Identify relevant pages/frames
4. If node IDs provided, focus on those nodes

### Step 3: Extract Design Tokens

From Figma file, extract:

**Colors:**
- Fill colors with names
- Stroke colors
- Effect colors (shadows)
- Text colors

**Typography:**
- Font families
- Font sizes
- Font weights
- Line heights
- Letter spacing

**Spacing:**
- Auto-layout gaps
- Padding values
- Common spacing patterns

**Effects:**
- Shadow definitions
- Blur effects
- Corner radius values

### Step 4: Extract Component Specs

For each component in Figma:
- Name and description
- Variants (if using Figma variants)
- Properties and their options
- Internal structure
- Interactive states (if documented)

### Step 5: Extract Layout Specs

Capture layout information:
- Frame dimensions
- Auto-layout settings
- Constraints
- Responsive behavior (if using Figma features)
- Grid systems

### Step 6: Generate Implementation Specs

Transform Figma data into implementation-ready format:

**Token Format:**
```css
/* Colors */
--color-primary: #3B82F6;
--color-secondary: #6B7280;

/* Spacing */
--spacing-xs: 4px;
--spacing-sm: 8px;

/* Typography */
--font-heading: 600 24px/1.2 'Inter';
```

**Component Format:**
```markdown
### ButtonComponent
**Variants:** primary, secondary, ghost
**Sizes:** sm, md, lg
**States:** default, hover, pressed, disabled
**Padding:** 8px 16px (md)
**Border Radius:** 6px
```

## Output Format

```markdown
## Figma Design Extraction: [File Name]

### Source
- **File:** [Figma file name]
- **URL:** [File URL]
- **Extracted:** [Timestamp]
- **Pages reviewed:** [List]

### Design Tokens

#### Colors
| Name | Hex | RGB | Usage |
|------|-----|-----|-------|
| Primary | #3B82F6 | 59, 130, 246 | Buttons, links |
| Primary Hover | #2563EB | 37, 99, 235 | Hover states |
| Text Primary | #111827 | 17, 24, 39 | Body text |
| Text Secondary | #6B7280 | 107, 114, 128 | Captions |
| Background | #FFFFFF | 255, 255, 255 | Page background |
| Surface | #F9FAFB | 249, 250, 251 | Cards, panels |
| Border | #E5E7EB | 229, 231, 235 | Dividers |
| Error | #EF4444 | 239, 68, 68 | Error states |
| Success | #10B981 | 16, 185, 129 | Success states |

#### Typography
| Style | Font | Size | Weight | Line Height | Letter Spacing |
|-------|------|------|--------|-------------|----------------|
| Heading 1 | Inter | 32px | 700 | 1.2 | -0.02em |
| Heading 2 | Inter | 24px | 600 | 1.3 | -0.01em |
| Body | Inter | 16px | 400 | 1.5 | 0 |
| Body Small | Inter | 14px | 400 | 1.5 | 0 |
| Caption | Inter | 12px | 400 | 1.4 | 0.01em |

#### Spacing Scale
| Token | Value | Usage |
|-------|-------|-------|
| 2xs | 2px | Minimal gaps |
| xs | 4px | Tight spacing |
| sm | 8px | Small gaps |
| md | 16px | Standard |
| lg | 24px | Section spacing |
| xl | 32px | Large gaps |
| 2xl | 48px | Page sections |

#### Effects
| Name | Type | Values |
|------|------|--------|
| Shadow SM | Drop shadow | 0 1px 2px rgba(0,0,0,0.05) |
| Shadow MD | Drop shadow | 0 4px 6px rgba(0,0,0,0.1) |
| Shadow LG | Drop shadow | 0 10px 15px rgba(0,0,0,0.1) |

#### Border Radius
| Token | Value |
|-------|-------|
| sm | 4px |
| md | 6px |
| lg | 8px |
| full | 9999px |

### Component Specifications

#### [ComponentName]
**Figma Node:** [Node ID]
**Variants:**
| Variant | Property | Values |
|---------|----------|--------|
| Style | variant | primary, secondary, ghost |
| Size | size | sm, md, lg |

**Dimensions:**
| Size | Width | Height | Padding |
|------|-------|--------|---------|
| sm | auto | 32px | 6px 12px |
| md | auto | 40px | 8px 16px |
| lg | auto | 48px | 12px 24px |

**States:**
| State | Background | Text | Border |
|-------|------------|------|--------|
| Default | Primary | White | None |
| Hover | Primary Hover | White | None |
| Pressed | Primary Dark | White | None |
| Disabled | Gray 200 | Gray 400 | None |

---

[Repeat for each component]

### Layout Specifications

#### [Frame/Screen Name]
**Dimensions:** [Width] x [Height]
**Auto-layout:** [Direction, gap, padding]
**Grid:** [If applicable]

**Structure:**
```
[Visual representation of layout structure]
```

### CSS Variables Export

```css
:root {
  /* Colors */
  --color-primary: #3B82F6;
  --color-primary-hover: #2563EB;
  --color-text-primary: #111827;
  --color-text-secondary: #6B7280;
  --color-background: #FFFFFF;
  --color-surface: #F9FAFB;
  --color-border: #E5E7EB;
  --color-error: #EF4444;
  --color-success: #10B981;

  /* Typography */
  --font-family: 'Inter', sans-serif;
  --font-size-xs: 12px;
  --font-size-sm: 14px;
  --font-size-base: 16px;
  --font-size-lg: 24px;
  --font-size-xl: 32px;

  /* Spacing */
  --spacing-2xs: 2px;
  --spacing-xs: 4px;
  --spacing-sm: 8px;
  --spacing-md: 16px;
  --spacing-lg: 24px;
  --spacing-xl: 32px;
  --spacing-2xl: 48px;

  /* Effects */
  --shadow-sm: 0 1px 2px rgba(0,0,0,0.05);
  --shadow-md: 0 4px 6px rgba(0,0,0,0.1);
  --shadow-lg: 0 10px 15px rgba(0,0,0,0.1);

  /* Border Radius */
  --radius-sm: 4px;
  --radius-md: 6px;
  --radius-lg: 8px;
  --radius-full: 9999px;
}
```

### Implementation Notes
- [Any Figma-specific patterns to note]
- [Limitations or areas needing interpretation]
- [Responsive considerations from design]
```

## Handoff Data

```json
{
  "figma_file": "[file name]",
  "tokens_extracted": {
    "colors": 12,
    "typography": 5,
    "spacing": 7,
    "effects": 3
  },
  "components_extracted": 8,
  "layouts_extracted": 4,
  "css_variables_generated": true
}
```

## MCP Not Available Response

If Figma MCP is not connected:

```markdown
## Figma Integration Not Available

I don't have access to Figma. To enable Figma integration:

1. **In Claude Desktop/Settings:**
   - Navigate to MCP Servers
   - Add Figma MCP
   - Authorize with your Figma account

2. **After connecting:**
   - Share the Figma file URL
   - I'll extract design tokens and component specs

**Proceed without Figma?**
I can design components based on the specification alone, using:
- Standard design patterns
- Constitution-defined tokens (if any)
- Industry-standard accessibility requirements

Would you like to:
- A) Connect Figma and return (recommended if you have designs)
- B) Proceed without Figma designs
```

## Human Checkpoint

**Tier:** Auto (extraction is read-only)

## Error Handling

| Error | Resolution |
|-------|------------|
| MCP not connected | Return connection instructions |
| File not accessible | Verify URL, check permissions |
| Node not found | List available nodes for selection |
| Extraction partial | Report what was extracted, note gaps |
