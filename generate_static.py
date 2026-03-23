#!/usr/bin/env python3
"""
Static Site Generator for Portfolio
Renders the Flask template with portfolio data to create static HTML files
"""

from flask import Flask, render_template
from pathlib import Path
import os
import shutil

# Import the portfolio data from app.py
# We'll copy the DEFAULT_PORTFOLIO from app.py
DEFAULT_PORTFOLIO = {
    'name': 'Hariharan Natarajan',
    'title': 'Lead Architect · Cloud Architect · GenAI Builder · Scrum Master · Product Owner · Project Manager · CyberSecurity Architect',
    'location': 'Stockholm, Sweden',
    'profile_picture': 'images/My Foto.jpeg',
    'bio': 'I am a Cloud Solutions Architect based in Stockholm, Sweden, helping enterprises adopt cloud, Cybersecurity, and GenAI.',
    'summary': 'Hari has 20+ years of IT experience including Analysis, Design, Architecture, Development of ERP and Cloud solutions. He has vast experience of Azure, AWS Public cloud and SAP. He has previously filled roles as senior Project manager, Scrum Master, Product Owner, Security architect and Lead solution architect. He has previously led globally distributed Cloud team with up to 30 Cloud Engg and Architect. He has a long background from SAP & public Cloud Architecture for Telia, Ericsson, H&M, Sandvik, Mersk, SAP AG, Jaguar, Commonwealth Bank and AGL.',  
    'experience_years': '20+',
    'certifications_count': '20X',
    'workshops_delivered': '10+',
    'contact': {
        'email': 'sivahari@gmail.com',
        'phone': '+46 763134148',
        'linkedin': 'www.linkedin.com/in/hariharan-natarajan-921b6a23/',
        'location': 'Stockholm, Sweden'
    },
    'about': {
        'location': 'Stockholm, Sweden',
        'languages': ['English', 'Swedish-Basic', 'Tamil'],
        'education': 'B.E. Computer Science',
        'currently_building': 'Azure enterprice landing zone and Cybersecurity tool'
    },
    'expertise': {
        'Azure Public Cloud': ['Enterprise Landing Zone Design', 'Application Architecture', 'Azure Entra/AD', 'Azure Functions', 'Azure Logic Apps', 'Azure DevOps', 'CI/CD', 'Data Factory', 'Data Lake', 'Synapse', 'Azure Defender', 'Azure Security Center'],
        'AWS Public Cloud': ['Landing Zone Design', 'CloudFormation', 'Security Hub', 'Control Tower', 'AWS WAF', 'IAM', 'EC2', 'EKS', 'Lambda'],
        'Cybersecurity & Compliance': ['NIS2 Directive', 'ISO 27001', 'PCI-DSS', 'NIST Framework', 'Azure Defender', 'AWS Security Hub', 'Identity Management', 'Zero Trust Architecture'],
        'GenAI & Machine Learning': ['Azure OpenAI', 'Azure Cognitive Search', 'RAG Architecture', 'LLM Deployment', 'AI Governance', 'Prompt Engineering', 'Agentic AI'],
        'Container & Orchestration': ['Kubernetes', 'Azure Kubernetes Service', 'Amazon EKS', 'Docker', 'Helm', 'Service Mesh', 'GitOps'],
        'HashiCorp Tools': ['Terraform', 'Consul', 'Vault', 'Service Mesh', 'Static Secrets', 'Dynamic Secrets'],
        'Infrastructure as Code': ['ARM Templates', 'Biceps', 'PowerShell Scripts', 'Terraform'],
        'DevOps & CI/CD': ['Azure DevOps', 'GitHub', 'GitLab', 'GitHub Actions', 'Automation'],
        'FinOps & Cloud Economics': ['Cloud Cost Analytics', 'Cost Optimization', 'Resource Utilization', 'Budget Management'],
        'SAP Expertise': ['SAP CRM', 'SAP Hybris C4C', 'SAP Workflow', 'ABAP Development', 'BOPF', 'Functional Consulting'],
        'Project Management': ['Agile Scrum Master', 'Product Owner', 'PSM I & II Certified', 'PSPO I & II Certified', 'Prince 2 Agile Foundation', 'Microsoft Project', 'RAID Log', 'RACI Matrix']
    },
    'experience': [
        {
            'title': 'Lead Solution and Cybersecurity Architect',
            'company': 'Capgemini Engg AB (Client: Telia)',
            'period': 'MAY 2024 – Present',
            'description': 'Azure and AWS Public Cloud - Design and implement Azure Landing Zone Architecture, Azure Entra Identity Management, NIS2/ISO/PCI-DSS Cybersecurity compliance, Azure Defender and NIST initiatives. AWS CloudFormation templates, Security Hub, Control Tower, WAF implementation. AI Chatbot POC for Landing Zone.'
        },
        {
            'title': 'Lead Architect & Cloud Advisor',
            'company': 'NordCloud Sweden AB (Client: Ericsson)',
            'period': 'AUG 2021 – Present',
            'description': 'Azure and AWS Public Cloud - Designed Azure Landing Zone with Entra/AD and PIM for global and China regions. Azure SSO sync with legacy AD. Coordinated product deliverables. AWS Landing Zone design with IAC templates for 10+ applications (EKS, EC2, Lambda). Security Hub and Control Tower implementation.'
        },
        {
            'title': 'Cloud Transformation Architect',
            'company': 'NordCloud Sweden AB (Client: Sandvik)',
            'period': 'AUG 2022 – Present',
            'description': 'Designed Active Directory, PIM, Monitoring, Patching and Backup solutions in Azure. Cloud transition strategy and roadmaps for Azure/AWS. Network and security landscape review. Data encryption and masking strategy for sensitive information.'
        },
        {
            'title': 'Solution Architect',
            'company': 'NordCloud Sweden AB (Client: H&M)',
            'period': 'JAN 2022 – AUG 2022',
            'description': 'Designed internal applications in Azure. Infrastructure as Code (Terraform) design and implementation. Mentored Cloud Engineers on Azure and Terraform.'
        },
        {
            'title': 'Lead Architect & Product Owner',
            'company': 'TATA Consultancy Services (Client: Ericsson)',
            'period': 'OCT 2019 – JULY 2021',
            'description': 'Agile coach and product owner for API factory and Common Cloud Service teams. Azure infrastructure modules and API application delivery. Designed Terraform IAC templates. Direct savings of 1.5M SEK/year in licensing.'
        },
        {
            'title': 'Agile Project Manager',
            'company': 'TATA Consultancy Services (Client: MERSK – APM Terminals)',
            'period': 'MAY 2019 – OCT 2019',
            'description': 'Project planning for IFS 10.0 Upgrade using Microsoft Project Professional. Resource management across work streams. RAID Log and RACI Matrix creation.'
        },
        {
            'title': 'SAP Architect, Onsite Lead & Scrum Master',
            'company': 'TATA Consultancy Services (Client: H&M, AGL, Kingfisher IT Services)',
            'period': 'JULY 2016 – MAY 2019',
            'description': 'Onsite coordinator for SAP CRM Marketing team. CLUB rollout, refactoring execution and planning. Customer information separation and Digital Receipt solution design.'
        },
        {
            'title': 'SAP Hybris C4C CRM/SD Consultant & Scrum Master',
            'company': 'TATA Consultancy Services (Client: Apple, Commonwealth Bank, Ashok Leyland, Jaguar Land Rover)',
            'period': 'OCT 2008 – JULY 2016',
            'description': 'SAP Hybris integration with SAP CRM. Technical team leadership and deliverable ownership. ODATA Interface design for SAP CRM opportunity screen with video conferencing.'
        },
        {
            'title': 'SAP BOPF ABAP Developer',
            'company': 'TATA Consultancy Services (Client: SAP AG)',
            'period': 'OCT 2007 – OCT 2008',
            'description': 'Developed three business objects in OOPS ABAP under Service Provider Cockpit work center of BYD project.'
        },
        {
            'title': 'SAP Workflow Architect',
            'company': 'L&T Infotech (Client: SAP AG)',
            'period': 'FEB 2007 – OCT 2007',
            'description': 'Designed workflow processes for electronic review and approvals in Non-Employee Personnel Change Request (PCR) scenarios in MSS.'
        },
        {
            'title': 'SAP ABAP Developer',
            'company': 'HCL Technology (Client: Mattson)',
            'period': 'MAR 2005 – FEB 2007',
            'description': 'Provided ABAP/4 support in the rollout and support of SAP R/3.'
        }
    ],
    'projects': [
        {
            'title': 'Azure enterprise landing zone in Terraform IaC',
            'description': 'End to End Automation of Onboarding and offboarding process in Azure Enterprice landing zone.',
            'status': 'LIVE',
            'technologies': ['Terraform', 'Azure', 'Infrastructure as Code', 'python']
        },
        {
            'title': 'AI Chatbot for Azure security and compliance',
            'description': 'AI-Powered Portfolio Analysis & Optimization tool',
            'status': 'Building',
            'technologies': ['Azure Foundation Models', 'Azure OpenAI', 'Azure Cognitive Search', 'Azure Functions', 'Python']
        }
    ],
    'certifications': [
        # Agile Project Management
        {'title': 'Prince 2 Agile Foundation', 'year': '', 'status': 'Certified'},
        # Professional Scrum
        {'title': 'Professional Scrum Product Owner I', 'year': '', 'status': 'Certified'},
        {'title': 'Professional Scrum Product Owner II', 'year': '', 'status': 'Certified'},
        {'title': 'Professional Scrum Master I', 'year': '', 'status': 'Certified'},
        {'title': 'Professional Scrum Master II', 'year': '', 'status': 'Certified'},
        # SAP Certifications
        {'title': 'SAP Certified App Associate - CRM Fundamentals', 'year': '', 'status': 'Certified'},
        {'title': 'SAP Certified Dev Associate - SAP Workflow with SAP NetWeaver', 'year': '', 'status': 'Certified'},
        # Azure Certifications
        {'title': 'Azure Solution Architect Expert', 'year': '', 'status': 'Certified'},
        {'title': 'Azure DevOps Engineer Expert', 'year': '', 'status': 'Certified'},
        {'title': 'Azure Cybersecurity Expert', 'year': '', 'status': 'Certified'},
        {'title': 'Azure Administrator Associate', 'year': '', 'status': 'Certified'},
        {'title': 'Azure Data Engineer Associate', 'year': '', 'status': 'Certified'},
        {'title': 'Azure Network Engineer Associate', 'year': '', 'status': 'Certified'},
        {'title': 'Azure Security Engineer Associate', 'year': '', 'status': 'Certified'},
        # AWS Certifications
        {'title': 'AWS Certified Solutions Architect', 'year': '', 'status': 'Certified'},
        {'title': 'AWS Certified Sys-Ops Administrator', 'year': '', 'status': 'Certified'},
        # HashiCorp Certifications
        {'title': 'HashiCorp Certified: Terraform', 'year': '', 'status': 'Certified'},
        {'title': 'HashiCorp Certified: Consul', 'year': '', 'status': 'Certified'},
        {'title': 'HashiCorp Certified: Vault', 'year': '', 'status': 'Certified'},
        # FinOps
        {'title': 'FinOps Certified Practitioner', 'year': '', 'status': 'Certified'}
    ],
    'speaking': {
        'workshops': '10+',
        'audience_reached': '100+',
        'events': ['NordCloud Tech Days', 'Azure Community Sweden']
    },
    'services': [
        {
            'title': 'Cloud Architecture & Migration',
            'description': 'Well-Architected reviews, migration roadmaps, landing zones, hybrid connectivity.'
        },
        {
            'title': 'GenAI Adoption & Application Development',
            'description': 'RAG, agentic AI, LLM deployment, AI governance, production GenAI apps.'
        },
        {
            'title': 'Kubernetes & Container Strategy',
            'description': 'EKS/OpenShift architecture, GitOps, service mesh, security, platform engineering.'
        },
        {
            'title': 'FinOps & Cloud Economics',
            'description': 'Rightsizing, reserved capacity, TCO modeling, cost governance.'
        }
    ]
}

def generate_static_site():
    """Generate static HTML files for GitHub Pages"""
    
    # Create Flask app for rendering
    app = Flask(__name__, 
                template_folder=str(Path(__file__).parent / 'templates'),
                static_folder=str(Path(__file__).parent / 'static'))
    
    # Configure for static generation
    app.config['SERVER_NAME'] = 'localhost'
    app.config['APPLICATION_ROOT'] = '/'
    app.config['PREFERRED_URL_SCHEME'] = 'http'
    
    with app.app_context():
        # Render the main page
        rendered_html = render_template('index.html', portfolio=DEFAULT_PORTFOLIO)

        # Convert absolute URLs to relative paths for GitHub Pages project deployment
        rendered_html = rendered_html.replace('http://localhost/static/css/style.css', 'static/css/style.css')
        rendered_html = rendered_html.replace('http://localhost/static/js/main.js', 'static/js/main.js')
        rendered_html = rendered_html.replace('/static/css/style.css', 'static/css/style.css')
        rendered_html = rendered_html.replace('/static/js/main.js', 'static/js/main.js')
        # Add more replacements if needed for other static files (images, fonts, etc.)
        
        # Ensure docs directory exists
        docs_dir = Path(__file__).parent / 'docs'
        docs_dir.mkdir(exist_ok=True)
        
        # Write the rendered HTML to docs/index.html
        with open(docs_dir / 'index.html', 'w', encoding='utf-8') as f:
            f.write(rendered_html)
        
        # Copy static files
        static_src = Path(__file__).parent / 'static'
        static_dest = docs_dir / 'static'
        
        if static_dest.exists():
            shutil.rmtree(static_dest)
        
        if static_src.exists():
            shutil.copytree(static_src, static_dest)
        
        print("Static site generated successfully!")
        print(f"Files created in: {docs_dir}")
        print("You can now commit and push these files to deploy to GitHub Pages")

if __name__ == '__main__':
    generate_static_site()