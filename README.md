# flask-api-template-healthcare 

## To do
- Now need to go in add in the linting (black? or the new rust one?)
- Now need to go in add in the testing (pytest)
- Now need to go in add the security checks of dependencies (safety, bandit, etc)

## HIPAA:

- RELEVANT - 1. Privacy Rule
- RELEVANT - 2. Security Rule
- NOT RELEVANT - 3. Enforcement Rule
- POT RELEVANT - 4. Breach Notification Rule
- POT RELEVANT - 5. Omnibus Rule
- RELEVANT - 6. Transaction and Code Sets Rule
- NOT RELEVANT - 7. Unique Identifiers Rule

[HITRUST](https://hitrustalliance.net/csf-license-agreement/) control v11.2.0

## FROM Excel Sheet HITRUST CSF v11.2.0 Cross Reference List

In total from security, privacy, and breach there are 137 (?) total unique HITRUST controls

### Unique HITRUST controls relevant for HIPAA Security Rule:
- 659 total control references for security rule
- 133 unique controls:

```
00.a Information Security Management Program	22
01.a Access Control Policy	15
01.b User Registration	9
01.c Privilege Management	12
01.d User Password Management	1
01.e Review of User Access Rights	2
01.f Password Use	1
01.g Unattended User Equipment	3
01.h Clear Desk and Clear Screen Policy	1
01.i Policy on the Use of Network Services	4
01.j User Authentication for External Connections	2
01.k Equipment Identification in Networks	2
01.l Remote Diagnostic and Configuration Port Protection	6
01.m Segregation in Networks	3
01.n Network Connection Control	4
01.o Network Routing Control	1
01.p Secure Log-on Procedures	3
01.q User Identification and Authentication	4
01.r Password Management System	1
01.t Session Time-out	1
01.u Limitation of Connection Time	1
01.v Information Access Restriction	7
01.w Sensitive System Isolation	1
01.x Mobile Computing and Communications	3
01.y Teleworking	5
02.a Roles and Responsibilities	8
02.b Screening	6
02.c Terms and Conditions of Employment	5
02.d Management Responsibilities	10
02.e Information Security Awareness, Education, and Training	9
02.f Disciplinary Process	4
02.g Termination or Change Responsibilities	1
02.h Return of Assets	1
02.i Removal of Access Rights	8
03.a Risk Management Program Development	5
03.b Performing Risk Assessments	7
03.c Risk Mitigation	3
03.d Risk Evaluation	1
04.a Information Security Policy Document	5
04.b Review of the Information Security Policy	4
05.a Management Commitment to Information Security	8
05.b Information Security Coordination	10
05.c Allocation of Information Security Responsibilities	4
05.d Authorization Process for Information Assets and Facilities	3
05.f Contact with Authorities	4
05.g Contact with Special Interest Groups	2
05.h Independent Review of Information Security	7
05.i Identification of Risks Related to External Parties	3
05.j Addressing Security When Dealing with Customers	4
05.k Addressing Security in Third Party Agreements	9
06.a Identification of Applicable Legislation	3
06.c Protection of Organizational Records	17
06.d Data Protection and Privacy of Covered Information	20
06.e Prevention of Misuse of Information Assets	4
06.f Regulation of Cryptographic Controls	4
06.g Compliance with Security Policies and Standards	3
06.h Technical Compliance Checking	5
06.i Information Systems Audit Controls	7
07.a Inventory of Assets	5
07.b Ownership of Assets	1
07.c Acceptable Use of Assets	1
07.d Classification Guidelines	5
08.a Physical Security Perimeter	5
08.b Physical Entry Controls	13
08.c Securing Offices, Rooms, and Facilities	3
08.e Working in Secure Areas	2
08.g Equipment Siting and Protection	4
08.i Cabling Security	3
08.j Equipment Maintenance	10
08.k Security of Equipment Off-Premises	2
08.l Secure Disposal or Re-Use of Equipment	5
08.m Removal of Property	1
09.a Documented Operations Procedures	1
09.aa Audit Logging	11
09.ab Monitoring System Use	15
09.ac Protection of Log Information	3
09.ad Administrator and Operator Logs	1
09.b Change Management	8
09.c Segregation of Duties	5
09.e Service Delivery	6
09.f Monitoring and Review of Third Party Services	5
09.h Capacity Management	2
09.i System Acceptance	3
09.j Controls Against Malicious Code	1
09.k Controls Against Mobile Code	1
09.l Back-up	7
09.m Network Controls	10
09.n Security of Network Services	5
09.o Management of Removable Media	7
09.p Disposal of Media	4
09.q Information Handling Procedures	11
09.r Security of System Documentation	1
09.s Information Exchange Policies and Procedures	9
09.t Exchange Agreements	1
09.u Physical Media in Transit	8
09.v Electronic Messaging	4
09.w Interconnected Business Information Systems	1
09.x Electronic Commerce Services	4
09.y On-line Transactions	4
09.z Publicly Available Information	3
10.a Security Requirements Analysis and Specification	8
10.b Input Data Validation	3
10.c Control of Internal Processing	11
10.d Message Integrity	1
10.f Policy on the Use of Cryptographic Controls	3
10.h Control of Operational Software	6
10.j Access Control to Program Source Code	1
10.k Change Control Procedures	4
10.m Control of Technical Vulnerabilities	7
11.a Reporting Information Security Events	8
11.b Reporting Security Weaknesses	3
11.c Responsibilities and Procedures	10
11.d Learning from Information Security Incidents	6
11.e Collection of Evidence	4
12.a Including Information Security in the Business Continuity Management Process	7
12.b Business Continuity and Risk Assessment	4
12.c Developing and Implementing Continuity Plans Including Information Security	14
12.d Business Continuity Planning Framework	4
12.e Testing, Maintaining and Re-Assessing Business Continuity Plans	5
13.a Privacy Notice	1
13.d Consent	1
13.e Choice	1
13.f Principle Access	5
13.j Data Minimization	1
13.k Use and Disclosure	13
13.l Retention and Disposal	2
13.p Governance	1
13.q Privacy and Impact Assessment	2
13.r Privacy Requirements for Contractors and Processors	12
13.t Privacy Protection Awareness and Training	2
```



### Unique HITRUST controls relevant for HIPAA Privacy Rule:
- 970 total control references for security rule
- 54 unique controls:

```
00.a Information Security Management Program	8
01.a Access Control Policy	1
01.c Privilege Management	2
01.w Sensitive System Isolation	1
02.a Roles and Responsibilities	1
02.b Screening	2
02.c Terms and Conditions of Employment	1
02.d Management Responsibilities	1
02.e Information Security Awareness, Education, and Training	6
02.f Disciplinary Process	3
02.i Removal of Access Rights	1
03.c Risk Mitigation	1
04.a Information Security Policy Document	2
04.b Review of the Information Security Policy	12
05.d Authorization Process for Information Assets and Facilities	1
05.e Confidentiality Agreements	2
05.f Contact with Authorities	1
05.i Identification of Risks Related to External Parties	2
05.j Addressing Security When Dealing with Customers	13
05.k Addressing Security in Third Party Agreements	3
06.a Identification of Applicable Legislation	5
06.c Protection of Organizational Records	36
06.d Data Protection and Privacy of Covered Information	18
06.e Prevention of Misuse of Information Assets	3
08.b Physical Entry Controls	1
09.aa Audit Logging	5
09.ab Monitoring System Use	1
09.c Segregation of Duties	1
09.e Service Delivery	2
09.n Security of Network Services	1
09.s Information Exchange Policies and Procedures	2
09.t Exchange Agreements	2
09.u Physical Media in Transit	2
09.x Electronic Commerce Services	1
10.a Security Requirements Analysis and Specification	2
10.c Control of Internal Processing	1
10.i Protection of System Test Data	1
11.a Reporting Information Security Events	10
11.e Collection of Evidence	1
13.a Privacy Notice	81
13.b Openness and Transparency	57
13.c Accounting of Disclosures	47
13.d Consent	56
13.e Choice	61
13.f Principle Access	97
13.j Data Minimization	75
13.k Use and Disclosure	277
13.l Retention and Disposal	5
13.n Participation and Redress	10
13.o Complaint Management	4
13.q Privacy and Impact Assessment	1
13.r Privacy Requirements for Contractors and Processors	30
13.t Privacy Protection Awareness and Training	8
13.u Privacy Protection Reporting	1
```

### Unique HITRUST controls relevant for HIPAA Breach Notification Rule:
- 34 total control references for security rule
- 5 unique controls:

```
03.b Performing Risk Assessments	1
06.c Protection of Organizational Records	2
11.a Reporting Information Security Events	28
11.c Responsibilities and Procedures	1
13.e Choice	1
```