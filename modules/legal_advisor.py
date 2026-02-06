"""
Legal Advisor Module
Provides general legal information based on user queries.
Integrated from lawyer.py Streamlit module into Flask architecture.
"""

# Enhanced legal knowledge base with detailed law references
LEGAL_KB = {
    "rent": {
        "title": "Rental Agreement & Tenant Rights",
        "points": [
            "A rental agreement is a contract between landlord and tenant defining terms of occupancy",
            "**Tenants have the right to peaceful possession** of the property during the lease period",
            "Landlords must provide habitable premises and cannot arbitrarily evict tenants",
            "**Written agreements are strongly recommended** though oral agreements are valid",
            "Security deposits must be returned (minus legitimate deductions) after lease ends",
            "Rent control laws vary by state - some cities have rent control boards"
        ],
        "laws": [
            {
                "name": "Transfer of Property Act, 1882",
                "section": "Section 105",
                "description": "Defines a lease of immovable property as a transfer of right to enjoy property for a certain time or in perpetuity, in consideration of a price paid or promised."
            },
            {
                "name": "State Rent Control Acts",
                "section": "Various sections",
                "description": "State-specific laws that regulate rent amounts, eviction procedures, and tenant protections. Each state has its own Rent Control Act with different provisions."
            },
            {
                "name": "Consumer Protection Act, 2019",
                "section": "Section 2(7)",
                "description": "Defines 'deficiency' in service, which can include landlord's failure to maintain property or provide agreed services to tenants."
            }
        ],
        "what_next": [
            "You can review your rental agreement to understand specific terms",
            "You can approach the local Rent Control Board if applicable in your city",
            "You can consult a property lawyer for agreement drafting or dispute resolution"
        ]
    },
    "tenant": {
        "title": "Rental Agreement & Tenant Rights",
        "points": [
            "A rental agreement is a contract between landlord and tenant defining terms of occupancy",
            "**Tenants have the right to peaceful possession** of the property during the lease period",
            "Landlords must provide habitable premises and cannot arbitrarily evict tenants",
            "**Written agreements are strongly recommended** though oral agreements are valid",
            "Security deposits must be returned (minus legitimate deductions) after lease ends",
            "Rent control laws vary by state - some cities have rent control boards"
        ],
        "laws": [
            {
                "name": "Transfer of Property Act, 1882",
                "section": "Section 105",
                "description": "Defines a lease of immovable property as a transfer of right to enjoy property for a certain time or in perpetuity, in consideration of a price paid or promised."
            },
            {
                "name": "State Rent Control Acts",
                "section": "Various sections",
                "description": "State-specific laws that regulate rent amounts, eviction procedures, and tenant protections. Each state has its own Rent Control Act with different provisions."
            },
            {
                "name": "Consumer Protection Act, 2019",
                "section": "Section 2(7)",
                "description": "Defines 'deficiency' in service, which can include landlord's failure to maintain property or provide agreed services to tenants."
            }
        ],
        "what_next": [
            "You can review your rental agreement to understand specific terms",
            "You can approach the local Rent Control Board if applicable in your city",
            "You can consult a property lawyer for agreement drafting or dispute resolution"
        ]
    },
    "landlord": {
        "title": "Rental Agreement & Tenant Rights",
        "points": [
            "A rental agreement is a contract between landlord and tenant defining terms of occupancy",
            "**Tenants have the right to peaceful possession** of the property during the lease period",
            "Landlords must provide habitable premises and cannot arbitrarily evict tenants",
            "**Written agreements are strongly recommended** though oral agreements are valid",
            "Security deposits must be returned (minus legitimate deductions) after lease ends",
            "Rent control laws vary by state - some cities have rent control boards"
        ],
        "laws": [
            {
                "name": "Transfer of Property Act, 1882",
                "section": "Section 105",
                "description": "Defines a lease of immovable property as a transfer of right to enjoy property for a certain time or in perpetuity, in consideration of a price paid or promised."
            },
            {
                "name": "State Rent Control Acts",
                "section": "Various sections",
                "description": "State-specific laws that regulate rent amounts, eviction procedures, and tenant protections. Each state has its own Rent Control Act with different provisions."
            },
            {
                "name": "Consumer Protection Act, 2019",
                "section": "Section 2(7)",
                "description": "Defines 'deficiency' in service, which can include landlord's failure to maintain property or provide agreed services to tenants."
            }
        ],
        "what_next": [
            "You can review your rental agreement to understand specific terms",
            "You can approach the local Rent Control Board if applicable in your city",
            "You can consult a property lawyer for agreement drafting or dispute resolution"
        ]
    },
    "consumer": {
        "title": "Consumer Rights & Protection",
        "points": [
            "**Consumers have the right to be protected** against unfair trade practices and defective goods",
            "Right to seek redressal for defective goods or deficient services",
            "Complaints can be filed in Consumer Forums (District, State, or National level)",
            "**E-commerce purchases are covered** under consumer protection laws",
            "Product liability provisions hold manufacturers accountable for defective products",
            "Consumers can claim compensation for loss, injury, or mental agony"
        ],
        "laws": [
            {
                "name": "Consumer Protection Act, 2019",
                "section": "Section 2(9)",
                "description": "Defines 'consumer' as any person who buys goods or avails services for consideration, excluding those for resale or commercial purposes."
            },
            {
                "name": "Consumer Protection Act, 2019",
                "section": "Section 84",
                "description": "Establishes product liability, making manufacturers, sellers, and service providers liable for harm caused by defective products or deficient services."
            },
            {
                "name": "Legal Metrology Act, 2009",
                "section": "Section 18",
                "description": "Regulates weights, measures, and packaged commodities to prevent consumer deception regarding quantity and quality."
            }
        ],
        "what_next": [
            "You can file a complaint with the Consumer Forum within 2 years of the cause of action",
            "You can gather evidence like bills, receipts, warranty cards, and communication records",
            "You can approach consumer helplines or consumer protection councils for guidance"
        ]
    },
    "defective": {
        "title": "Consumer Rights & Protection",
        "points": [
            "**Consumers have the right to be protected** against unfair trade practices and defective goods",
            "Right to seek redressal for defective goods or deficient services",
            "Complaints can be filed in Consumer Forums (District, State, or National level)",
            "**E-commerce purchases are covered** under consumer protection laws",
            "Product liability provisions hold manufacturers accountable for defective products",
            "Consumers can claim compensation for loss, injury, or mental agony"
        ],
        "laws": [
            {
                "name": "Consumer Protection Act, 2019",
                "section": "Section 2(9)",
                "description": "Defines 'consumer' as any person who buys goods or avails services for consideration, excluding those for resale or commercial purposes."
            },
            {
                "name": "Consumer Protection Act, 2019",
                "section": "Section 84",
                "description": "Establishes product liability, making manufacturers, sellers, and service providers liable for harm caused by defective products or deficient services."
            },
            {
                "name": "Legal Metrology Act, 2009",
                "section": "Section 18",
                "description": "Regulates weights, measures, and packaged commodities to prevent consumer deception regarding quantity and quality."
            }
        ],
        "what_next": [
            "You can file a complaint with the Consumer Forum within 2 years of the cause of action",
            "You can gather evidence like bills, receipts, warranty cards, and communication records",
            "You can approach consumer helplines or consumer protection councils for guidance"
        ]
    },
    "marriage": {
        "title": "Marriage & Matrimonial Rights",
        "points": [
            "Marriage is a legal union governed by personal laws based on religion",
            "**Both parties must give free and valid consent** - forced marriages are voidable",
            "**Minimum age is 21 for men and 18 for women** (as per current law)",
            "Registration of marriage is mandatory in most states for legal proof",
            "Hindu Marriage Act applies to Hindus, Buddhists, Jains, and Sikhs",
            "Special Marriage Act allows inter-faith and civil marriages"
        ],
        "laws": [
            {
                "name": "Hindu Marriage Act, 1955",
                "section": "Section 5",
                "description": "Specifies the conditions for a valid Hindu marriage, including age, consent, mental soundness, and prohibited degrees of relationship."
            },
            {
                "name": "Special Marriage Act, 1954",
                "section": "Section 4",
                "description": "Allows civil marriages irrespective of religion, subject to legal conditions like age, consent, and notice period."
            },
            {
                "name": "Constitution of India",
                "section": "Article 21",
                "description": "Guarantees the right to life and personal liberty, which courts have interpreted to include the right to choose a spouse and marry freely."
            }
        ],
        "what_next": [
            "You can register your marriage with the local registrar or municipal authority",
            "You can obtain a marriage certificate which serves as legal proof",
            "You can consult a family lawyer for pre-nuptial agreements or marriage-related queries"
        ]
    },
    "divorce": {
        "title": "Divorce & Separation",
        "points": [
            "Divorce dissolves a marriage legally and requires court proceedings",
            "**Grounds include cruelty, adultery, desertion, mental disorder**, and others",
            "**Mutual consent divorce requires 6-month cooling period** and is faster",
            "Contested divorce can take several years depending on case complexity",
            "Alimony and child custody are determined based on case circumstances",
            "Mediation and counseling are often encouraged before final decree"
        ],
        "laws": [
            {
                "name": "Hindu Marriage Act, 1955",
                "section": "Section 13",
                "description": "Lists grounds for divorce including adultery, cruelty, desertion for two years, conversion to another religion, mental disorder, and communicable diseases."
            },
            {
                "name": "Hindu Marriage Act, 1955",
                "section": "Section 13B",
                "description": "Provides for divorce by mutual consent if parties have lived separately for one year and agree that they cannot live together."
            },
            {
                "name": "Special Marriage Act, 1954",
                "section": "Section 27",
                "description": "Allows divorce on similar grounds as Hindu Marriage Act for marriages registered under Special Marriage Act."
            }
        ],
        "what_next": [
            "You can explore mediation or counseling services before filing for divorce",
            "You can gather evidence and documentation if filing contested divorce",
            "You can consult a family lawyer to understand your rights regarding alimony and custody"
        ]
    },
    "property": {
        "title": "Property Rights & Inheritance",
        "points": [
            "Property can be acquired through purchase, inheritance, or gift",
            "**Registration of property documents is mandatory** for immovable property",
            "**Hindu Succession Act grants equal rights to sons and daughters** in ancestral property",
            "Ancestral property has different rules than self-acquired property",
            "Wills must be executed properly; registered wills are preferred",
            "Stamp duty and registration fees vary by state"
        ],
        "laws": [
            {
                "name": "Transfer of Property Act, 1882",
                "section": "Section 54",
                "description": "Requires that sale of immovable property worth more than ₹100 must be made by registered document signed by both parties."
            },
            {
                "name": "Hindu Succession Act, 1956",
                "section": "Section 6",
                "description": "Provides that daughters have equal coparcenary rights in ancestral property, same as sons, since the 2005 amendment."
            },
            {
                "name": "Registration Act, 1908",
                "section": "Section 17",
                "description": "Mandates registration of documents relating to transfer of immovable property to make them legally valid and admissible as evidence."
            }
        ],
        "what_next": [
            "You can verify property ownership through title search and encumbrance certificate",
            "You can consult a property lawyer before purchasing or transferring property",
            "You can register property documents at the local sub-registrar office"
        ]
    },
    "inheritance": {
        "title": "Property Rights & Inheritance",
        "points": [
            "Property can be acquired through purchase, inheritance, or gift",
            "**Registration of property documents is mandatory** for immovable property",
            "**Hindu Succession Act grants equal rights to sons and daughters** in ancestral property",
            "Ancestral property has different rules than self-acquired property",
            "Wills must be executed properly; registered wills are preferred",
            "Stamp duty and registration fees vary by state"
        ],
        "laws": [
            {
                "name": "Transfer of Property Act, 1882",
                "section": "Section 54",
                "description": "Requires that sale of immovable property worth more than ₹100 must be made by registered document signed by both parties."
            },
            {
                "name": "Hindu Succession Act, 1956",
                "section": "Section 6",
                "description": "Provides that daughters have equal coparcenary rights in ancestral property, same as sons, since the 2005 amendment."
            },
            {
                "name": "Registration Act, 1908",
                "section": "Section 17",
                "description": "Mandates registration of documents relating to transfer of immovable property to make them legally valid and admissible as evidence."
            }
        ],
        "what_next": [
            "You can verify property ownership through title search and encumbrance certificate",
            "You can consult a property lawyer before purchasing or transferring property",
            "You can register property documents at the local sub-registrar office"
        ]
    },
    "employment": {
        "title": "Employment Rights & Labor Laws",
        "points": [
            "**Employees are entitled to minimum wages** as per state regulations",
            "Working hours, overtime, and leave are regulated by labor laws",
            "**Employers must provide safe working conditions** and social security benefits",
            "Termination must follow due process; arbitrary dismissal can be challenged",
            "Employees can form unions and engage in collective bargaining",
            "Sexual harassment complaints are handled by Internal Complaints Committee (ICC)"
        ],
        "laws": [
            {
                "name": "Industrial Disputes Act, 1947",
                "section": "Section 25F",
                "description": "Requires employers to give one month's notice or wages in lieu, and severance pay when terminating employees who have completed one year of service."
            },
            {
                "name": "Minimum Wages Act, 1948",
                "section": "Section 3",
                "description": "Empowers government to fix minimum wages for scheduled employments to prevent exploitation of workers."
            },
            {
                "name": "Employees' Provident Funds Act, 1952",
                "section": "Section 6",
                "description": "Mandates contribution to provident fund for employees' retirement security in establishments with 20 or more employees."
            }
        ],
        "what_next": [
            "You can check your employment contract and company policies for specific terms",
            "You can approach labor commissioner or labor court for workplace disputes",
            "You can join or form employee unions for collective representation"
        ]
    },
    "labor": {
        "title": "Employment Rights & Labor Laws",
        "points": [
            "**Employees are entitled to minimum wages** as per state regulations",
            "Working hours, overtime, and leave are regulated by labor laws",
            "**Employers must provide safe working conditions** and social security benefits",
            "Termination must follow due process; arbitrary dismissal can be challenged",
            "Employees can form unions and engage in collective bargaining",
            "Sexual harassment complaints are handled by Internal Complaints Committee (ICC)"
        ],
        "laws": [
            {
                "name": "Industrial Disputes Act, 1947",
                "section": "Section 25F",
                "description": "Requires employers to give one month's notice or wages in lieu, and severance pay when terminating employees who have completed one year of service."
            },
            {
                "name": "Minimum Wages Act, 1948",
                "section": "Section 3",
                "description": "Empowers government to fix minimum wages for scheduled employments to prevent exploitation of workers."
            },
            {
                "name": "Employees' Provident Funds Act, 1952",
                "section": "Section 6",
                "description": "Mandates contribution to provident fund for employees' retirement security in establishments with 20 or more employees."
            }
        ],
        "what_next": [
            "You can check your employment contract and company policies for specific terms",
            "You can approach labor commissioner or labor court for workplace disputes",
            "You can join or form employee unions for collective representation"
        ]
    },
    "workplace": {
        "title": "Employment Rights & Labor Laws",
        "points": [
            "**Employees are entitled to minimum wages** as per state regulations",
            "Working hours, overtime, and leave are regulated by labor laws",
            "**Employers must provide safe working conditions** and social security benefits",
            "Termination must follow due process; arbitrary dismissal can be challenged",
            "Employees can form unions and engage in collective bargaining",
            "Sexual harassment complaints are handled by Internal Complaints Committee (ICC)"
        ],
        "laws": [
            {
                "name": "Industrial Disputes Act, 1947",
                "section": "Section 25F",
                "description": "Requires employers to give one month's notice or wages in lieu, and severance pay when terminating employees who have completed one year of service."
            },
            {
                "name": "Minimum Wages Act, 1948",
                "section": "Section 3",
                "description": "Empowers government to fix minimum wages for scheduled employments to prevent exploitation of workers."
            },
            {
                "name": "Employees' Provident Funds Act, 1952",
                "section": "Section 6",
                "description": "Mandates contribution to provident fund for employees' retirement security in establishments with 20 or more employees."
            }
        ],
        "what_next": [
            "You can check your employment contract and company policies for specific terms",
            "You can approach labor commissioner or labor court for workplace disputes",
            "You can join or form employee unions for collective representation"
        ]
    },
    "harassment": {
        "title": "Workplace Harassment & POSH Act",
        "points": [
            "**Sexual harassment at workplace is a criminal offense**",
            "Every organization with 10+ employees must have an Internal Complaints Committee",
            "**Complaints must be filed within 3 months** of the incident",
            "Employers must provide a safe and harassment-free environment",
            "Victims have the right to confidentiality and protection from retaliation",
            "Penalties include compensation and disciplinary action against the harasser"
        ],
        "laws": [
            {
                "name": "Sexual Harassment of Women at Workplace Act, 2013",
                "section": "Section 2(n)",
                "description": "Defines sexual harassment to include unwelcome physical contact, demand for sexual favors, sexually colored remarks, showing pornography, or any other unwelcome conduct."
            },
            {
                "name": "Sexual Harassment of Women at Workplace Act, 2013",
                "section": "Section 4",
                "description": "Mandates every employer to constitute an Internal Complaints Committee to receive and address complaints of sexual harassment."
            },
            {
                "name": "Indian Penal Code, 1860",
                "section": "Section 354A",
                "description": "Criminalizes sexual harassment with punishment of imprisonment up to three years or fine or both."
            }
        ],
        "what_next": [
            "You can file a written complaint with the Internal Complaints Committee of your organization",
            "You can approach the Local Complaints Committee if your workplace doesn't have an ICC",
            "You can also file a police complaint under IPC Section 354A for criminal proceedings"
        ]
    },
    "cheque": {
        "title": "Cheque Bounce & Negotiable Instruments",
        "points": [
            "**Dishonor of cheque due to insufficient funds is a criminal offense**",
            "Payee must send a legal notice within 30 days of cheque bounce",
            "**Drawer has 15 days to make payment** after receiving notice",
            "Complaint can be filed in court if payment is not made",
            "Punishment includes fine up to twice the cheque amount and/or imprisonment",
            "Civil remedies are also available for recovery of the amount"
        ],
        "laws": [
            {
                "name": "Negotiable Instruments Act, 1881",
                "section": "Section 138",
                "description": "Makes dishonor of cheque for insufficiency of funds a criminal offense punishable with imprisonment up to two years or fine up to twice the cheque amount."
            },
            {
                "name": "Negotiable Instruments Act, 1881",
                "section": "Section 142",
                "description": "Provides that offenses under Section 138 are compoundable, meaning parties can settle the matter outside court with court's permission."
            },
            {
                "name": "Code of Civil Procedure, 1908",
                "section": "Order 37",
                "description": "Provides for summary suits for recovery of money based on negotiable instruments, allowing faster civil remedies."
            }
        ],
        "what_next": [
            "You can send a legal demand notice to the drawer within 30 days of cheque bounce",
            "You can file a criminal complaint under Section 138 if payment is not made within 15 days",
            "You can also file a civil suit for recovery of the cheque amount"
        ]
    },
    "accident": {
        "title": "Motor Vehicle Accident Claims",
        "points": [
            "**Victims of road accidents can claim compensation** for injuries or death",
            "Claims can be filed before Motor Accident Claims Tribunal (MACT)",
            "**Third-party insurance is mandatory** for all vehicles",
            "Compensation depends on injury severity, income loss, and medical expenses",
            "Hit-and-run cases can claim from Motor Vehicle Accident Fund",
            "Time limit for filing claim is typically 6 months to 3 years"
        ],
        "laws": [
            {
                "name": "Motor Vehicles Act, 1988",
                "section": "Section 166",
                "description": "Provides for application to Claims Tribunal for compensation in case of death or permanent disablement due to motor vehicle accident."
            },
            {
                "name": "Motor Vehicles Act, 1988",
                "section": "Section 146",
                "description": "Mandates third-party insurance for all motor vehicles to cover liability for death, bodily injury, or property damage."
            },
            {
                "name": "Fatal Accidents Act, 1855",
                "section": "Section 1A",
                "description": "Allows legal representatives of deceased to claim compensation for loss of dependency and support due to wrongful death."
            }
        ],
        "what_next": [
            "You can file a claim petition before the Motor Accident Claims Tribunal",
            "You can gather evidence like FIR, medical reports, income proof, and accident photos",
            "You can consult a lawyer specializing in motor accident claims for proper valuation"
        ]
    },
    "cyber": {
        "title": "Cyber Crime & Digital Rights",
        "points": [
            "**Cyber crimes include hacking, identity theft, phishing, and online fraud**",
            "Victims can file complaints with local police or Cyber Crime Cell",
            "Data privacy is protected under Information Technology Act and DPDP Act",
            "**Unauthorized access to computer systems is punishable**",
            "Online defamation and harassment are actionable offenses",
            "Digital evidence must be preserved properly for legal proceedings"
        ],
        "laws": [
            {
                "name": "Information Technology Act, 2000",
                "section": "Section 66",
                "description": "Punishes computer-related offenses like hacking with imprisonment up to three years or fine up to ₹5 lakh."
            },
            {
                "name": "Information Technology Act, 2000",
                "section": "Section 43",
                "description": "Provides for compensation for unauthorized access, data theft, virus introduction, or damage to computer systems."
            },
            {
                "name": "Digital Personal Data Protection Act, 2023",
                "section": "Section 8",
                "description": "Grants individuals rights over their personal data including right to access, correction, erasure, and grievance redressal."
            }
        ],
        "what_next": [
            "You can file a complaint at the National Cyber Crime Reporting Portal (cybercrime.gov.in)",
            "You can preserve all digital evidence like screenshots, emails, and transaction records",
            "You can approach your bank immediately if it involves financial fraud"
        ]
    },
    "privacy": {
        "title": "Data Privacy & Protection",
        "points": [
            "**Individuals have the right to privacy as a fundamental right**",
            "Organizations must obtain consent before collecting personal data",
            "**Data must be used only for specified purposes** and stored securely",
            "Individuals can request access, correction, or deletion of their data",
            "Data breaches must be reported to authorities and affected individuals",
            "Cross-border data transfer has specific compliance requirements"
        ],
        "laws": [
            {
                "name": "Digital Personal Data Protection Act, 2023",
                "section": "Section 6",
                "description": "Requires data fiduciaries to obtain valid consent before processing personal data and use it only for specified purposes."
            },
            {
                "name": "Constitution of India",
                "section": "Article 21",
                "description": "Supreme Court has recognized right to privacy as a fundamental right intrinsic to life and personal liberty."
            },
            {
                "name": "Information Technology Act, 2000",
                "section": "Section 72A",
                "description": "Punishes disclosure of personal information without consent by any person including intermediaries, with imprisonment up to three years."
            }
        ],
        "what_next": [
            "You can request organizations to delete or correct your personal data",
            "You can file complaints with the Data Protection Board for violations",
            "You can review privacy policies before sharing personal information online"
        ]
    },
    "defamation": {
        "title": "Defamation & Reputation Rights",
        "points": [
            "**Defamation is injury to reputation through false statements**",
            "Can be civil (damages) or criminal (imprisonment and fine)",
            "Statement must be published to third parties and identify the victim",
            "**Truth, fair comment, and privilege are valid defenses**",
            "Online defamation on social media is also actionable",
            "Burden of proof lies on the plaintiff in civil cases"
        ],
        "laws": [
            {
                "name": "Indian Penal Code, 1860",
                "section": "Section 499",
                "description": "Defines defamation as making or publishing imputation concerning any person intending to harm reputation, except in cases covered by exceptions."
            },
            {
                "name": "Indian Penal Code, 1860",
                "section": "Section 500",
                "description": "Prescribes punishment for defamation with imprisonment up to two years or fine or both."
            },
            {
                "name": "Information Technology Act, 2000",
                "section": "Section 66A (struck down)",
                "description": "Previously criminalized offensive online messages but was struck down by Supreme Court in 2015 for being unconstitutional and vague."
            }
        ],
        "what_next": [
            "You can send a legal notice demanding retraction and apology",
            "You can file a civil defamation suit for monetary damages",
            "You can file a criminal complaint for defamation under IPC Sections 499-500"
        ]
    },
    "domestic violence": {
        "title": "Domestic Violence Protection",
        "points": [
            "**Domestic violence includes physical, emotional, sexual, and economic abuse**",
            "Women can file complaints under Protection of Women from Domestic Violence Act",
            "Protection Officers and Service Providers assist victims",
            "**Victims can seek protection orders, residence orders, and monetary relief**",
            "Complaints can be filed at police station or magistrate court",
            "Shelter homes and counseling services are available for victims"
        ],
        "laws": [
            {
                "name": "Protection of Women from Domestic Violence Act, 2005",
                "section": "Section 3",
                "description": "Defines domestic violence broadly to include physical, sexual, verbal, emotional, and economic abuse by any adult male member of shared household."
            },
            {
                "name": "Protection of Women from Domestic Violence Act, 2005",
                "section": "Section 12",
                "description": "Empowers Magistrate to pass protection orders, residence orders, monetary relief, custody orders, and compensation orders."
            },
            {
                "name": "Indian Penal Code, 1860",
                "section": "Section 498A",
                "description": "Criminalizes cruelty by husband or his relatives with punishment of imprisonment up to three years and fine."
            }
        ],
        "what_next": [
            "You can approach Protection Officer or Service Provider for assistance",
            "You can file a complaint with the Magistrate or police station",
            "You can seek shelter at government-run protection homes or NGOs"
        ]
    },
    "will": {
        "title": "Wills & Testamentary Succession",
        "points": [
            "**A will is a legal document expressing how property should be distributed after death**",
            "Any person of sound mind above 18 years can make a will",
            "**Registration is not mandatory but highly recommended** for authenticity",
            "Wills can be modified or revoked at any time during the testator's lifetime",
            "Two witnesses are required for execution of a will",
            "Probate may be required in certain states for will enforcement"
        ],
        "laws": [
            {
                "name": "Indian Succession Act, 1925",
                "section": "Section 59",
                "description": "Defines a will as the legal declaration of intention of a testator regarding property disposition after death."
            },
            {
                "name": "Indian Succession Act, 1925",
                "section": "Section 63",
                "description": "Prescribes formalities for execution of unprivileged wills including signature of testator and attestation by two witnesses."
            },
            {
                "name": "Registration Act, 1908",
                "section": "Section 18",
                "description": "Allows optional registration of wills, which provides additional authenticity and prevents loss or tampering."
            }
        ],
        "what_next": [
            "You can draft a will clearly identifying beneficiaries and property details",
            "You can register your will at the sub-registrar office for added security",
            "You can consult a lawyer to ensure the will is legally valid and unambiguous"
        ]
    },
    "fir": {
        "title": "FIR & Criminal Complaints",
        "points": [
            "**First Information Report (FIR) is the first step in criminal proceedings**",
            "Police are obligated to register FIR for cognizable offenses",
            "**FIR can be filed at any police station**; jurisdictional transfer happens later",
            "Copy of FIR must be provided free of cost to the complainant",
            "Zero FIR can be filed at any police station regardless of jurisdiction",
            "False FIR can lead to legal consequences for the complainant"
        ],
        "laws": [
            {
                "name": "Bharatiya Nagarik Suraksha Sanhita, 2023",
                "section": "Section 173",
                "description": "Mandates that information about cognizable offenses must be recorded in writing, signed by informant, and registered as FIR."
            },
            {
                "name": "Bharatiya Nagarik Suraksha Sanhita, 2023",
                "section": "Section 173(2)",
                "description": "Requires that a copy of the FIR be provided to the informant free of cost immediately after registration."
            },
            {
                "name": "Indian Penal Code, 1860",
                "section": "Section 182",
                "description": "Punishes giving false information to public servant with intent to cause investigation, with imprisonment up to six months or fine."
            }
        ],
        "what_next": [
            "You can file an FIR at the nearest police station for cognizable offenses",
            "You can request a copy of the FIR immediately after registration",
            "You can approach the Magistrate if police refuse to register FIR"
        ]
    }
}


def legal_advice(question):
    """
    Main API function for legal advice.
    Processes user question and returns legal information.
    
    INPUT:
        question (str): User's legal question
    
    OUTPUT:
        {
            "success": True/False,
            "matched": True/False,
            "title": str,
            "answer": str (formatted HTML),
            "law_reference": list of dicts,
            "what_next": list of str,
            "disclaimer": str,
            "keyword": str (matched keyword)
        }
    """
    if not question or question.strip() == "":
        return {
            "success": False,
            "error": "Please enter a question to get legal information."
        }
    
    # Convert to lowercase for matching
    question_lower = question.lower()
    
    # Find matching topic - improved matching logic
    matched_topic = None
    matched_keyword = None
    
    # First try exact word match
    question_words = question_lower.split()
    for keyword in LEGAL_KB:
        if keyword in question_words:
            matched_topic = LEGAL_KB[keyword]
            matched_keyword = keyword
            break
    
    # If no exact match, try partial match (keyword contained in question)
    if not matched_topic:
        for keyword in LEGAL_KB:
            if keyword in question_lower:
                matched_topic = LEGAL_KB[keyword]
                matched_keyword = keyword
                break
    
    # Build response
    if matched_topic:
        # Format answer as HTML bullet points
        answer_html = "<ul class='legal-points'>"
        for point in matched_topic['points']:
            # Convert markdown bold to HTML
            point_html = point.replace("**", "<strong>").replace("**", "</strong>")
            answer_html += f"<li>{point_html}</li>"
        answer_html += "</ul>"
        
        return {
            "success": True,
            "matched": True,
            "title": matched_topic['title'],
            "answer": answer_html,
            "law_reference": matched_topic['laws'],
            "what_next": matched_topic.get('what_next', []),
            "disclaimer": "⚠️ DISCLAIMER: This information is for educational purposes only and does not constitute legal advice. Consult a licensed lawyer for your specific situation.",
            "keyword": matched_keyword
        }
    else:
        # No match found
        available_topics = ", ".join(sorted(set([LEGAL_KB[k]['title'] for k in LEGAL_KB])))
        return {
            "success": True,
            "matched": False,
            "message": "The topic you're asking about is not currently in our knowledge base.",
            "available_topics": available_topics,
            "disclaimer": "⚠️ For specific legal advice, please consult a licensed lawyer."
        }
