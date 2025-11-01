#!/usr/bin/env python3
"""
Create a sample pitch deck for testing PitchDeck Autopilot.
"""

from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter

def create_sample_deck(filename="sample_deck.pdf"):
    """Create a sample startup pitch deck."""
    c = canvas.Canvas(filename, pagesize=letter)
    width, height = letter
    
    # Slide 1 - Title
    c.setFont("Helvetica-Bold", 28)
    c.drawString(100, 700, "Acme Robotics")
    c.setFont("Helvetica", 20)
    c.drawString(100, 650, "AI-Native Robotics Platform")
    c.setFont("Helvetica", 14)
    c.drawString(100, 600, "Seed Round Pitch Deck - Q1 2024")
    c.showPage()
    
    # Slide 2 - Problem
    c.setFont("Helvetica-Bold", 24)
    c.drawString(100, 750, "The Problem")
    c.setFont("Helvetica", 16)
    c.drawString(100, 700, "Industrial robots are expensive and data-hungry")
    c.setFont("Helvetica", 14)
    c.drawString(120, 670, "• Training requires 6-12 months of real-world data collection")
    c.drawString(120, 645, "• Deployment costs exceed $500K per robot")
    c.drawString(120, 620, "• Each new task requires complete retraining")
    c.drawString(120, 595, "• Limited adaptability to changing environments")
    c.showPage()
    
    # Slide 3 - Solution
    c.setFont("Helvetica-Bold", 24)
    c.drawString(100, 750, "Our Solution")
    c.setFont("Helvetica", 16)
    c.drawString(100, 700, "Synthetic data generation for rapid robot training")
    c.setFont("Helvetica", 14)
    c.drawString(120, 670, "• Proprietary simulation environment")
    c.drawString(120, 645, "• 10x faster deployment than traditional methods")
    c.drawString(120, 620, "• 80% cost reduction in training phase")
    c.drawString(120, 595, "• Transfer learning across multiple tasks")
    c.showPage()
    
    # Slide 4 - Product
    c.setFont("Helvetica-Bold", 24)
    c.drawString(100, 750, "Product")
    c.setFont("Helvetica", 16)
    c.drawString(100, 700, "End-to-end robotics training platform")
    c.setFont("Helvetica", 14)
    c.drawString(120, 670, "1. Synthetic Data Generator")
    c.drawString(140, 645, "   - Physics-based simulation")
    c.drawString(140, 620, "   - Realistic environment modeling")
    c.drawString(120, 585, "2. Training Engine")
    c.drawString(140, 560, "   - Reinforcement learning algorithms")
    c.drawString(140, 535, "   - Transfer learning capabilities")
    c.drawString(120, 500, "3. Deployment Tools")
    c.drawString(140, 475, "   - Real-time adaptation")
    c.drawString(140, 450, "   - Performance monitoring")
    c.showPage()
    
    # Slide 5 - Traction
    c.setFont("Helvetica-Bold", 24)
    c.drawString(100, 750, "Traction")
    c.setFont("Helvetica", 16)
    c.drawString(100, 700, "Early adoption and strong pipeline")
    c.setFont("Helvetica", 14)
    c.drawString(120, 670, "• 2 pilot customers in automotive manufacturing")
    c.drawString(120, 645, "• $250K in committed ARR for 2025")
    c.drawString(120, 620, "• 15,000 hours of simulation data generated")
    c.drawString(120, 595, "• 5 additional LOIs in advanced discussions")
    c.drawString(120, 570, "• 95% customer satisfaction score")
    c.showPage()
    
    # Slide 6 - Team
    c.setFont("Helvetica-Bold", 24)
    c.drawString(100, 750, "Team")
    c.setFont("Helvetica", 16)
    c.drawString(100, 700, "World-class robotics and AI expertise")
    c.setFont("Helvetica", 14)
    c.drawString(120, 670, "Sarah Chen - CEO")
    c.drawString(140, 645, "   • Ex-DeepMind, led robotics research team")
    c.drawString(140, 620, "   • PhD in Robotics from MIT")
    c.drawString(120, 585, "Mike Rodriguez - CTO")
    c.drawString(140, 560, "   • Former Tesla Autopilot engineer")
    c.drawString(140, 535, "   • MS in Computer Science from Stanford")
    c.drawString(120, 500, "Advisory Board:")
    c.drawString(140, 475, "   • Prof. James Lee (MIT Robotics Lab)")
    c.drawString(140, 450, "   • Dr. Emily Watson (Google AI)")
    c.showPage()
    
    # Slide 7 - Market
    c.setFont("Helvetica-Bold", 24)
    c.drawString(100, 750, "Market Opportunity")
    c.setFont("Helvetica", 16)
    c.drawString(100, 700, "Large and rapidly growing market")
    c.setFont("Helvetica", 14)
    c.drawString(120, 670, "TAM: $8.3B addressable market")
    c.drawString(120, 645, "SAM: $2.1B serviceable market")
    c.drawString(120, 620, "SOM: $210M serviceable obtainable market (10% of SAM)")
    c.drawString(120, 585, "Market Growth:")
    c.drawString(140, 560, "   • Growing at 19% CAGR")
    c.drawString(140, 535, "   • Accelerated by labor shortage")
    c.drawString(140, 510, "   • Driven by AI advances")
    c.showPage()
    
    # Slide 8 - Business Model
    c.setFont("Helvetica-Bold", 24)
    c.drawString(100, 750, "Business Model")
    c.setFont("Helvetica", 16)
    c.drawString(100, 700, "SaaS + Usage-based pricing")
    c.setFont("Helvetica", 14)
    c.drawString(120, 670, "Revenue Streams:")
    c.drawString(140, 645, "   • Platform subscription: $50K-$200K/year")
    c.drawString(140, 620, "   • Simulation credits: $0.10 per hour")
    c.drawString(140, 595, "   • Professional services: $200/hour")
    c.drawString(120, 560, "Unit Economics:")
    c.drawString(140, 535, "   • Average contract value: $150K")
    c.drawString(140, 510, "   • Gross margin: 85%")
    c.drawString(140, 485, "   • CAC payback: 9 months")
    c.showPage()
    
    # Slide 9 - Competition
    c.setFont("Helvetica-Bold", 24)
    c.drawString(100, 750, "Competitive Landscape")
    c.setFont("Helvetica", 16)
    c.drawString(100, 700, "Clear differentiation in the market")
    c.setFont("Helvetica", 14)
    c.drawString(120, 670, "Traditional Robotics Companies:")
    c.drawString(140, 645, "   • Slow, expensive manual training")
    c.drawString(140, 620, "   • Limited adaptability")
    c.drawString(120, 585, "Simulation Software Vendors:")
    c.drawString(140, 560, "   • Generic tools, not robotics-specific")
    c.drawString(140, 535, "   • No end-to-end training solution")
    c.drawString(120, 500, "Our Advantage:")
    c.drawString(140, 475, "   • 10x faster training")
    c.drawString(140, 450, "   • Integrated platform")
    c.drawString(140, 425, "   • Proprietary transfer learning")
    c.showPage()
    
    # Slide 10 - Moat
    c.setFont("Helvetica-Bold", 24)
    c.drawString(100, 750, "Competitive Moat")
    c.setFont("Helvetica", 16)
    c.drawString(100, 700, "Strong defensibility")
    c.setFont("Helvetica", 14)
    c.drawString(120, 670, "Technology:")
    c.drawString(140, 645, "   • Proprietary simulation engine (3 years of R&D)")
    c.drawString(140, 620, "   • 2 patents filed, 3 more in process")
    c.drawString(120, 585, "Data:")
    c.drawString(140, 560, "   • Growing dataset of robot behaviors")
    c.drawString(140, 535, "   • Network effects from each deployment")
    c.drawString(120, 500, "Partnerships:")
    c.drawString(140, 475, "   • Strategic relationships with robot manufacturers")
    c.showPage()
    
    # Slide 11 - Financials
    c.setFont("Helvetica-Bold", 24)
    c.drawString(100, 750, "Financial Projections")
    c.setFont("Helvetica", 16)
    c.drawString(100, 700, "Path to profitability")
    c.setFont("Helvetica", 14)
    c.drawString(120, 670, "2024: $250K revenue")
    c.drawString(120, 645, "2025: $1.2M revenue (380% growth)")
    c.drawString(120, 620, "2026: $4.5M revenue (275% growth)")
    c.drawString(120, 595, "2027: $12M revenue (167% growth)")
    c.drawString(120, 560, "Break-even expected: Q3 2026")
    c.showPage()
    
    # Slide 12 - Ask
    c.setFont("Helvetica-Bold", 24)
    c.drawString(100, 750, "The Ask")
    c.setFont("Helvetica", 18)
    c.drawString(100, 700, "Raising $2M Seed Round")
    c.setFont("Helvetica", 14)
    c.drawString(120, 670, "Use of Funds:")
    c.drawString(140, 645, "   • Engineering: $1.0M (50%)")
    c.drawString(140, 620, "   • Sales & Marketing: $600K (30%)")
    c.drawString(140, 595, "   • Operations: $400K (20%)")
    c.drawString(120, 560, "Milestones:")
    c.drawString(140, 535, "   • 10 paying customers by Q4 2024")
    c.drawString(140, 510, "   • $1M ARR by Q2 2025")
    c.drawString(140, 485, "   • Series A ready by Q4 2025")
    c.showPage()
    
    # Slide 13 - Risks
    c.setFont("Helvetica-Bold", 24)
    c.drawString(100, 750, "Key Risks & Mitigation")
    c.setFont("Helvetica", 14)
    c.drawString(120, 710, "Technology Risk:")
    c.drawString(140, 685, "   • Sim-to-real transfer may not generalize")
    c.drawString(140, 660, "   • Mitigation: Extensive testing, gradual rollout")
    c.drawString(120, 625, "Market Risk:")
    c.drawString(140, 600, "   • Slow enterprise adoption")
    c.drawString(140, 575, "   • Mitigation: Focus on early adopters, pilot programs")
    c.drawString(120, 540, "Competitive Risk:")
    c.drawString(140, 515, "   • Large players entering the space")
    c.drawString(140, 490, "   • Mitigation: Speed to market, IP protection")
    c.showPage()
    
    # Slide 14 - Contact
    c.setFont("Helvetica-Bold", 28)
    c.drawString(100, 700, "Thank You")
    c.setFont("Helvetica", 18)
    c.drawString(100, 650, "Let's Build the Future of Robotics")
    c.setFont("Helvetica", 14)
    c.drawString(100, 600, "Sarah Chen - CEO")
    c.drawString(100, 575, "sarah@acmerobotics.ai")
    c.drawString(100, 550, "+1 (415) 555-0123")
    c.drawString(100, 515, "www.acmerobotics.ai")
    c.showPage()
    
    c.save()
    print(f"✅ Created {filename} with 14 slides")
    print(f"\nTo analyze the deck, run:")
    print(f"  python main.py {filename}")
    print(f"\nOr in fast mode (no API):")
    print(f"  python main.py {filename} --fast")


if __name__ == "__main__":
    create_sample_deck()


