courses = {
    "University of South Florida": {
        "ACG": {
            "2021": {
                "Class Full Name": "Principles of Financial Accounting",
                "Description": "Study of basic accounting principles including the recording and reporting of financial activity. The preparation and interpretation of financial statements.",
                "CoReqs": "N/A",
                "Prereqs": "N/A",
                "Credit Hours": 3
            },
            "2071": {
                "Class Full Name": "Principles of Managerial Accounting",
                "Description": "A study of the accountant\u2019s role in assisting management in the planning and controlling of business activities.",
                "CoReqs": "N/A",
                "Prereqs": [
                    {
                        "Department": "ACG",
                        "Course Code": "2021",
                        "Grade": "C"
                    }
                ],
                "Credit Hours": 3
            },
            "3074": {
                "Class Full Name": "Managerial Accounting for Non-Business Majors",
                "Description": "The study of the uses of accounting data internally by managers in planning and controlling the affairs of organizations.",
                "Mingrade_coreq": "N/A",
                "Prereqs": "N/A",
                "Credit Hours": 3
            },
            "3103": {
                "Class Full Name": "Intermediate Financial Accounting I",
                "Description": "Theory and methodology underlying financial reporting, including the FASB\u2019s conceptual framework, the accounting process, financial statements, accounting changes, present value applications, and current assets.",
                "CoReqs": [
                    {
                        "Department": "ACG",
                        "Course Code": "3341",
                        "Grade": "C"
                    }
                ],
                "Mingrade_coreq": "N/A",
                "Prereqs": "N/A",
                "Credit Hours": 3
            },
            "3341": {
                "Class Full Name": "Cost Accounting and Control I",
                "Description": "Deals with cost accounting systems for different entities, cost behavior patterns, cost-volume-profit analysis, relevant information for decision making, and budgets and standard costs for planning and control.",
                "Prereqs": {
                    "AND": [
                        {
                            "OR": [
                                {
                                    "Department": "ACG",
                                    "Course Code": "2021",
                                    "Grade": "C"
                                },
                                {
                                    "Department": "ACG",
                                    "Course Code": "2021C",
                                    "Grade": "C"
                                },
                                {
                                    "AND": [
                                        {
                                            "Department": "ACG",
                                            "Course Code": "2001",
                                            "Grade": "C"
                                        },
                                        {
                                            "Department": "ACG",
                                            "Course Code": "2011",
                                            "Grade": "C"
                                        }
                                    ]
                                }
                            ]
                        },
                        {
                            "Department": "ACG",
                            "Course Code": "2071",
                            "Grade": "C"
                        }
                    ]
                },
                "Coreqs": {
                    "AND": [
                        {
                            "Department": "ACG",
                            "Course Code": "3103",
                            "Grade": "C"
                        }
                    ]
                },
                "Credit Hours": 3
            }
        },
        "EEL": {
            "4835": {
                "Class Full Name": "Programming Design",
                "Description": "This course provides essential knowledge for engineering students to design computer programs to solve various tasks in real-world applications.",
                "Prereqs": {
                    "AND": [
                        {
                            "Department": "EEL",
                            "Course Code": "2161",
                            "Grade": "N/A"
                        }
                    ]
                },
                "Coreqs": "N/A",
                "Credit Hours": 3
            },
            "2161": {
                "Class Full Name": "Programming with C",
                "Description": "An introductory course to provide the fundamentals of computer language for electrical engineering students. Skills on syntax, functions, data, input and output, algorithm, and creating solutions for engineering problems using C.",
                "Prereqs": "N/A",
                "Coreqs": "N/A",
                "Credit Hours": 3
            },
            "3163C": {
                "Class Full Name": "Computer Tool Lab",
                "Description": "An introductory course to provide the knowledge on using Matlab and Simulink for solving wide range of problems in the field of electrical engineering - differential equation, convolution, Fourier Series and Transform, Laplace Transform, DSP, and etc.",
                "Prereqs": {
                    "AND": [
                        {
                            "Department": "EEL",
                            "Course Code": "2161",
                            "Grade": "C"
                        }
                    ]
                },
                "Coreqs": {
                    "AND": [
                        {
                            "Department": "EEL",
                            "Course Code": "4102",
                            "Grade": "C"
                        }
                    ]
                },
                "Credit Hours": 1
            },
            "3705": {
                "Class Full Name": "Fundamentals of Digital Circuits",
                "Description": "Binary number systems; truth functions; Boolean algebra; canonical forms; minimization of combinational logic circuits; synchronous and Asynchronous logic circuits. HDL\u00b4s introduction.",
                "Prereqs": "N/A",
                "Coreqs": "N/A",
                "Credit Hours": 3
            },
            "3705L": {
                "Class Full Name": "Fundamentals of Digital Circuits Laboratory",
                "Description": "Develop designs and demonstrate logic concepts. Schematic capture for design implementation, simulation and design verification.",
                "Prereqs": {
                    "AND": [
                        {
                            "Department": "EEL",
                            "Course Code": "3705",
                            "Grade": "C"
                        }
                    ]
                },
                "Coreqs": "N/A",
                "Credit Hours": 1
            },
            "4102": {
                "Class Full Name": "Signals and Systems",
                "Description": "Provides further study in the analysis of signals and linear systems. Includes time and frequency domain points of view such as Laplace and Fourier analysis as well as convolution.",
                "Prereqs": {
                    "AND": [
                        {
                            "Department": "EGN",
                            "Course Code": "3402",
                            "Grade": "C"
                        },
                        {
                            "Department": "EGN",
                            "Course Code": "3374",
                            "Grade": "C"
                        }
                    ]
                },
                "Coreqs": {
                    "AND": [
                        {
                            "Department": "EEL",
                            "Course Code": "3163C",
                            "Grade": "C"
                        },
                        {
                            "Department": "EGN",
                            "Course Code": "3374",
                            "Grade": "C"
                        }
                    ]
                },
                "Credit Hours": 3
            },
            "3100": {
                "Class Full Name": "Network Analysis and Design",
                "Description": "A third cource in linear circuit analysis and design. Transient and steady-state responses of passive RLC networks to various functions.",
                "Prereqs": {
                    "AND": [
                        {
                            "Department": "EGN",
                            "Course Code": "3420",
                            "Grade": "C"
                        },
                        {
                            "Department": "EGN",
                            "Course Code": "3374",
                            "Grade": "B"
                        }
                    ]
                },
                "Coreqs": "N/A",
                "Credit Hours": 3
            },
            "3115L": {
                "Class Full Name": "Laboratory I",
                "Description": "Basic circuit theory applications; computer-aided design tools, electrical measurement techniques.",
                "Prereqs": {
                    "AND": [
                        {
                            "Department": "EGN",
                            "Course Code": "3373",
                            "Grade": "C"
                        }
                    ]
                },
                "Coreqs": "N/A",
                "Credit Hours": 1
            },
            "3116L": {
                "Class Full Name": "Laboratory II",
                "Description": "This larboratory is designed to introduce electrical engineering students to the design, building and testing of active electronic networks. Computer Aided Design tools and computer data acquistition strategies are examined in greater detail.",
                "Prereqs": {
                    "AND": [
                        {
                            "Department": "EEE",
                            "Course Code": "3302",
                            "Grade": "C"
                        },
                        {
                            "Department": "EEL",
                            "Course Code": "3115L",
                            "Grade": "C"
                        }
                    ]
                },
                "Coreqs": "N/A",
                "Credit Hours": 1
            },
            "3472C": {
                "Class Full Name": "Electrical Engineering Science II",
                "Description": "Electromagnetic field theory, including charge distributions, static and dynamic electromagnetic fields, transmission lines and dynamic electromagnetic fields, transmission lines and optics.",
                "Prereqs": {
                    "AND": [
                        {
                            "Department": "EGN",
                            "Course Code": "3420",
                            "Grade": "C"
                        },
                        {
                            "Department": "EEE",
                            "Course Code": "3394",
                            "Grade": "C"
                        }
                    ]
                },
                "Coreqs": "N/A",
                "Credit Hours": 4
            },
            "4206L": {
                "Class Full Name": "Electromechanical Energy System Lab",
                "Description": "This course aiiims to provide students with hands-on experience related to Electric Mechanical Conversion Systems.",
                "Prereqs": {
                    "AND": [
                        {
                            "Department": "EGN",
                            "Course Code": "3374",
                            "Grade": "C"
                        }
                    ]
                },
                "Coreqs": {
                    "AND": [
                        {
                            "Department": "EGN",
                            "Course Code": "3375",
                            "Grade": "C"
                        }
                    ]
                },
                "Credit Hours": 1
            },
            "4212": {
                "Class Full Name": "Energy Delivery Systems",
                "Description": "The course provides the students the fundamentals and analysis of the electric power delivery system to facilitate the integration of distributed energy resources, e.g. solar energy.",
                "Prereqs": {
                    "AND": [
                        {
                            "Department": "EEL",
                            "Course Code": "4241",
                            "Grade": "C"
                        }
                    ]
                },
                "Coreqs": "N/A",
                "Credit Hours": 3
            },
            "4224": {
                "Class Full Name": "Electric Machines and Drives",
                "Description": "This course examines power electronic for motor control. AC motor control objectives and realization through power electronic converters will be discussed and validated through MATLAB/Simpowersystems based circuit simulation.",
                "Prereqs": {
                    "AND": [
                        {
                            "Department": "EGN",
                            "Course Code": "3375",
                            "Grade": "C"
                        },
                        {
                            "Department": "EEL",
                            "Course Code": "4241",
                            "Grade": "C"
                        }
                    ]
                },
                "Coreqs": "N/A",
                "Credit Hours": 3
            },
            "4241": {
                "Class Full Name": "Power Electronics",
                "Description": "This course topologies used to convert electricity from one form to another. The course will emphasize switch mode building blocks, variety of converters based on the building block, Pulse Width Modultation based control, and applications.",
                "Prereqs": {
                    "OR": [
                        {
                            "Department": "EGN",
                            "Course Code": "3373",
                            "Grade": "C"
                        },
                        {
                            "Department": "EGN",
                            "Course Code": "3374",
                            "Grade": "C"
                        }
                    ]
                },
                "Coreqs": "N/A",
                "Credit Hours": 3
            },
            "4271": {
                "Class Full Name": "Power System Protection",
                "Description": "Protection philosophy;electromechanical and picroprocessor relays; device coordination; instrument transformers; distance and differenial relays; non-radial line, transformer, and generator/motor protection.",
                "Prereqs": {
                    "AND": [
                        {
                            "Department": "EGN",
                            "Course Code": "3375",
                            "Grade": "C"
                        },
                        {
                            "Department": "EEL",
                            "Course Code": "4213",
                            "Grade": "C"
                        }
                    ]
                },
                "Coreqs": "N/A",
                "Credit Hours": 3
            },
            "4251": {
                "Class Full Name": "Power System Analysis",
                "Description": "This course will introduce analysis and operation of power systems. The topics covered in this course include per unit system, load flow analysis, voltage stability, economic dispatch, state estimation and power system economics.",
                "Prereqs": {
                    "AND": [
                        {
                            "Department": "EGN",
                            "Course Code": "3374",
                            "Grade": "C"
                        },
                        {
                            "Department": "EGN",
                            "Course Code": "3375",
                            "Grade": "C"
                        }
                    ]
                },
                "Coreqs": "N/A",
                "Credit Hours": 3
            },
            "4421": {
                "Class Full Name": "RF/Microwave Circuits I",
                "Description": "Introduction to passive microwave circuit design.Investigate the characteristics of transmission lines used in modern microwave systems, the tools used for analysis, and some common circuit topologies for matching, filtering and power distribution. Part one of a two-part sequence. EE majors only. Not available on S/U basis.",
                "Prereqs": {
                    "AND": [
                        {
                            "Department": "EEL",
                            "Course Code": "4423C",
                            "Grade": "C"
                        }
                    ]
                },
                "Coreqs": "N/A",
                "Credit Hours": 3
            },
            "4422": {
                "Class Full Name": "RF/Microwave Circuits II",
                "Description": "Introduction to active RF/Microwve circuit design. Investigate the characteristics of amplifiers and oscillators used in modern microwave systems, the tools used for analysis, and some common circuit topologies for biasing and matching. Substantial coverage of stability analysis, constant gain methods and noise figure. Part two of a two-part sequence. EE majors only. Not available on an S/U basis.",
                "Prereqs": {
                    "AND": [
                        {
                            "Department": "EEL",
                            "Course Code": "4421",
                            "Grade": "C"
                        }
                    ]
                },
                "Coreqs": "N/A",
                "Credit Hours": 3
            },
            "4423C": {
                "Class Full Name": "Wireless Circuits & Systems Design Laboratory",
                "Description": "An extensive hands-on intnroduction to wireless radio frequency and microwave circuits and systems, involveing modern measurements, fabrication and computer-aided design experiences at both component and syb-system levels. Not available on S/U basis",
                "Prereqs": {
                    "AND": [
                        {
                            "Department": "EEL",
                            "Course Code": "3472C",
                            "Grade": "C"
                        }
                    ]
                },
                "Coreqs": "N/A",
                "Credit Hours": 3
            },
            "4461": {
                "Class Full Name": "Antenna Theory",
                "Description": "Fundamental principles of antennas and application of EM theory for antenna analysis and design. Different types of antennas and their applications are introduced with particular focus on linear, loop, match antennas and antenna arrays.",
                "Prereqs": {
                    "AND": [
                        {
                            "Department": "EEL",
                            "Course Code": "3472C",
                            "Grade": "C"
                        },
                        {
                            "Department": "EEL",
                            "Course Code": "4423C",
                            "Grade": "C"
                        }
                    ]
                },
                "Coreqs": "N/A",
                "Credit Hours": 3
            },
            "4512C": {
                "Class Full Name": "Introduction to Communication Systems",
                "Description": "Provides and introduction to the fundamental principles and techniques of analog and digital communications systems. Theory is put into practice by investigating a variety of applications. Lectures and projects develop understanding of modern communication systems design and analysis",
                "Prereqs": {
                    "AND": [
                        {
                            "Department": "EEL",
                            "Course Code": "4102",
                            "Grade": "C"
                        }
                    ]
                },
                "Coreqs": "N/A",
                "Credit Hours": 3
            },
            "4540": {
                "Class Full Name": "Radar Systems",
                "Description": "The course provides a comprehensive introduction to radar systems and applications. The course examines radar concepts at both the systems and the syb-system level. Electromagnetic propagation, scattering, and antenna concepts are discussed. Wireless system design, signal processing, and radar imaging topics are analyzed.",
                "Prereqs": {
                    "AND": [
                        {
                            "Department": "EEL",
                            "Course Code": "4423C",
                            "Grade": "C"
                        }
                    ]
                },
                "Coreqs": "N/A",
                "Credit Hours": 3
            },
            "4657": {
                "Class Full Name": "Linear Control Systems",
                "Description": "Analysis and design of linear feedback controls systems. State Variable descriptions to include block diagrams, signal-flow graphs, stability, outh Hurwitz analysis, Root Locus methods, Bode plots, PID compensators, & introduction to  full-state feedback",
                "Prereqs": {
                    "OR": [
                        {
                            "Department": "EEL",
                            "Course Code": "3472C",
                            "Grade": "C"
                        },
                        {
                            "AND": [
                                {
                                    "Department": "PHY",
                                    "Course Code": "2049",
                                    "Grade": "C"
                                },
                                {
                                    "Department": "PHY",
                                    "Course Code": "2049L",
                                    "Grade": "C"
                                }
                            ]
                        }
                    ]
                },
                "Coreqs": "N/A",
                "Credit Hours": 3
            },
            "4657L": {
                "Class Full Name": "Linear Control Systems Laboratory",
                "Description": "This laboratory introduces students to the techniques needed for the design and implementation of automatic industrial control systems. Students will learn the basics of the software and hardware used for the design and implementation of control systems.",
                "Prereqs": "N/A",
                "Coreqs": {
                    "AND": [
                        {
                            "Department": "EEL",
                            "Course Code": "4657",
                            "Grade": "C"
                        }
                    ]
                },
                "Credit Hours": 1
            },
            "4680": {
                "Class Full Name": "Applied Mechatronics",
                "Description": "This course present mechatronics as the integration of mechanical & electrical systems, electronics, computer softare and control systems via multidisciplinary applications to promot innovation.",
                "Prereqs": {
                    "AND": [
                        {
                            "Department": "EEL",
                            "Course Code": "4657",
                            "Grade": "C"
                        }
                    ]
                },
                "Coreqs": "N/A",
                "Credit Hours": 3
            },
            "4727C": {
                "Class Full Name": "Digital Signal Processing with Field Programmable",
                "Description": "Development of real-time digital signal processing systems from algorithm to hardware using DSP, FPGA, and hybrid DSP/FPGA rapid prototyping platforms. The course has both leacture and laboratory components.",
                "Prereqs": {
                    "AND": [
                        {
                            "Department": "EEL",
                            "Course Code": "4102",
                            "Grade": "C"
                        },
                        {
                            "Department": "EEL",
                            "Course Code": "4512C",
                            "Grade": "C"
                        }
                    ]
                },
                "Coreqs": "N/A",
                "Credit Hours": 3
            },
            "4740": {
                "Class Full Name": "Embedded Systems",
                "Description": "This course covers the principles of hardare and softare design for higher-end embedded systems inherenet in many hardware platforms and applications being developed for engineering and science.",
                "Prereqs": {
                    "AND": [
                        {
                            "Department": "EEL",
                            "Course Code": "2161",
                            "Grade": "C"
                        },
                        {
                            "Department": "EEL",
                            "Course Code": "3705L",
                            "Grade": "C"
                        }
                    ]
                },
                "Coreqs": "N/A",
                "Credit Hours": 3
            },
            "4743L": {
                "Class Full Name": "Microprocessor Laboratory",
                "Description": "Application of microprocessors and microcontrollers for data entry, processing, display and real time signal input/output and control.",
                "Prereqs": "N/A",
                "Coreqs": {
                    "AND": [
                        {
                            "Department": "EEL",
                            "Course Code": "4744",
                            "Grade": "C"
                        }
                    ]
                },
                "Credit Hours": 1
            },
            "4744": {
                "Class Full Name": "Microprocessor Principles and Applications",
                "Description": "Functional Description, Arithmetic and Logic capabilities. Control and Timing. Interrupts and priority sytems. Software design and documentation. Distributed function processing",
                "Prereqs": {
                    "AND": [
                        {
                            "Department": "EEL",
                            "Course Code": "3705",
                            "Grade": "C-"
                        }
                    ]
                },
                "Coreqs": "N/A",
                "Credit Hours": 3
            },
            "4756": {
                "Class Full Name": "Digital Signal Processing",
                "Description": "Sampling and quantization of signals; frequency-domain representations, transforms;digital filtering filter structures; DFT;fft; multi-rate processing, Special analysis.",
                "Prereqs": {
                    "AND": [
                        {
                            "Department": "EEL",
                            "Course Code": "4102",
                            "Grade": "C"
                        }
                    ]
                },
                "Coreqs": "N/A",
                "Credit Hours": 3
            },
            "4782": {
                "Class Full Name": "Data Networks and Systems and Security",
                "Description": "The objective of this course is to provide a technical and operational introduction to data/computer communication networks, including network management and security.",
                "Prereqs": {
                    "AND": [
                        {
                            "Department": "EEL",
                            "Course Code": "2161",
                            "Grade": "C"
                        }
                    ]
                },
                "Coreqs": "N/A",
                "Credit Hours": 3
            },
            "4914": {
                "Class Full Name": "EE Deisgn 2",
                "Description": "Students apply the knowledge acquired in the classroom to design a system which meets a predetermined set of specifications. Students work individually or in small groups with a faculty member (project director) in their area of interest. (Majors Only.)",
                "Prereqs": {
                    "AND": [
                        {
                            "Department": "EEL",
                            "Course Code": "4906",
                            "Grade": "C"
                        }
                    ]
                },
                "Coreqs": "N/A",
                "Credit Hours": 3
            },
            "4940": {
                "Class Full Name": "Undergraduate Internship Experience",
                "Description": "This course will be used to assess and ultimately assign credit for students demonstrating the application of professional engineering knowledge and skills in off-campus internship placements.",
                "Prereqs": "N/A",
                "Coreqs": "N/A",
                "Credit Hours": 0
            },
            "4915": {
                "Class Full Name": "Advanced Undergraduate Research Experience",
                "Description": "This class is a supervised research experience offered for undergraduates in chemical engineering. There is no syllabus for the class. Learning outcomes are determined by the supervising faculty member and documented in a departmental contract research form.",
                "Prereqs": {
                    "AND": [
                        {
                            "Department": "EGS",
                            "Course Code": "2070",
                            "Grade": "C"
                        }
                    ]
                },
                "Coreqs": "N/A",
                "Credit Hours": 0
            },
            "4872": {
                "Class Full Name": "AI and Security in Cyber Physical Systems",
                "Description": "This course will introduce challenges and opportunities in the use of artificial intelligence (AI) in cyber physical systems (CPSs). The course will provide students with skills to design and analyze CPSs that are intelligent, autonomous, reliable, secure and privacy preserving with the help of AI technologies. Various examples of CPSs and AI technologies will be discussed in different application domains including smart cities, smart grids, vehicular networks, health and biomedical systems, and robotics systems with a focus on their security aspects.",
                "Prereqs": {
                    "AND": [
                        {
                            "Department": "EEL",
                            "Course Code": "4835",
                            "Grade": "C"
                        }
                    ]
                },
                "Coreqs": "N/A",
                "Credit Hours": 3
            },
            "4010": {
                "Class Full Name": "MAKE Hands-On Engineering Design",
                "Description": "The primary objective of the course is to introduce students to the creative design of devices following the engineering design process. The course will teach students the essential design skills needed for the design of \u201cmechatronic\u201d devices (i.e. devices incorporating electronic, mechanical and software based components). After taking this course students will have basic knowledge in computer aided design, electronic circuit development, programming concepts and control systems",
                "Prereqs": "N/A",
                "Coreqs": "N/A",
                "Credit Hours": 3
            },
            "4030": {
                "Class Full Name": "Electrical Systems Environments",
                "Description": "Dynamics, vibration, thermodynamics, and heat transfer in electrical, electronic, and electromechanical systems and their environments.",
                "Prereqs": {
                    "AND": [
                        {
                            "Department": "MAP",
                            "Course Code": "2302",
                            "Grade": "C"
                        },
                        {
                            "Department": "PHY",
                            "Course Code": "2049",
                            "Grade": "C"
                        }
                    ]
                },
                "Coreqs": "N/A",
                "Credit Hours": 3
            },
            "4213": {
                "Class Full Name": "Industrial Power Distribution 1",
                "Description": "Prepares the student to design electrical power systems for industrial applications. Source configurations, transformer connections, symmetrical and asymmetrical fault calculations, protective device sizing, arc flash calculations.",
                "Prereqs": {
                    "AND": [
                        {
                            "Department": "EGN",
                            "Course Code": "3375",
                            "Grade": "C"
                        }
                    ]
                },
                "Coreqs": "N/A",
                "Credit Hours": 3
            },
            "4214": {
                "Class Full Name": "Electric (Utility) Distribution Systems",
                "Description": "Familiarizes the student with electric utility power distribution systems. Modeling loads; distribution transformers; subtransmission lines, substations, and distribution primary and secondary; power system calcs, voltage regulation, protection methods.",
                "Prereqs": {
                    "AND": [
                        {
                            "Department": "EGN",
                            "Course Code": "3375",
                            "Grade": "C"
                        },
                        {
                            "Department": "EEL",
                            "Course Code": "4213",
                            "Grade": "C"
                        }
                    ]
                },
                "Coreqs": "N/A",
                "Credit Hours": 3
            },
            "4258": {
                "Class Full Name": "Industrial Power Distribution 2",
                "Description": "Prepares the student to design electrical power systems for industrial applications. Raceway design, switchgear and motor control centers, ladder logic, motor application, lighting systems.",
                "Prereqs": {
                    "AND": [
                        {
                            "Department": "EEL",
                            "Course Code": "4213",
                            "Grade": "C"
                        }
                    ]
                },
                "Coreqs": "N/A",
                "Credit Hours": 3
            },
            "4283": {
                "Class Full Name": "Sustainable Energy",
                "Description": "This course aims to introduce students to concepts of sustainable energy conversion. Solar, wind, hydroelectricity, hydrogen, biomass and geothermal energy conversion methods as well as main storage technologies will be discussed.",
                "Prereqs": "N/A",
                "Coreqs": "N/A",
                "Credit Hours": 3
            },
            "4420": {
                "Class Full Name": "RF & Microwave Measurements",
                "Description": "This course introduces students to the theory and applications of modern radio frequency and microwave measurements. Topics to be included are network analyzer, spectrum analyzer, noise, power, and non-linear distortion measurements. Modern trends also treated are the use of on-wafer measurements for transistor characterization and the evaluation of monolithic microwave integrated circuits.",
                "Prereqs": {
                    "AND": [
                        {
                            "Department": "EEL",
                            "Course Code": "4423L",
                            "Grade": "C"
                        }
                    ]
                },
                "Coreqs": "N/A",
                "Credit Hours": 2
            },
            "4567": {
                "Class Full Name": "Electro-Optics",
                "Description": "An introduction to the field of electro-optics, including visible and infra-red sources and detectors, radiometry, optical and electronic components, and fiber optics.",
                "Prereqs": {
                    "OR": [
                        {
                            "Department": "EEL",
                            "Course Code": "3472C",
                            "Grade": "C"
                        },
                        {
                            "AND": [
                                {
                                    "Department": "PHY",
                                    "Course Code": "2049",
                                    "Grade": "C"
                                },
                                {
                                    "Department": "PHY",
                                    "Course Code": "2049L",
                                    "Grade": "C"
                                }
                            ]
                        }
                    ]
                },
                "Coreqs": "N/A",
                "Credit Hours": 3
            },
            "4595": {
                "Class Full Name": "Mobile and Personal Communication",
                "Description": "Providing the students with a comprehensive knowledge of most technical aspects, operations, and applications of second/third/fourth generations and future cellular mobile and personal communication technology.",
                "Prereqs": "N/A",
                "Coreqs": "N/A",
                "Credit Hours": 3
            },
            "4635": {
                "Class Full Name": "Digital Control Systems",
                "Description": "Review of linear control systems, sampling process, discrete time linear systems analysis,  Z-transforms, modeling and design of digital control systems, digital implementation of  analog controller, state space representation, concepts of observability and controllability,  concepts of nonlinear digital controls and optimal controls.",
                "Prereqs": {
                    "AND": [
                        {
                            "Department": "EEL",
                            "Course Code": "4657",
                            "Grade": "C"
                        }
                    ]
                },
                "Coreqs": "N/A",
                "Credit Hours": 3
            },
            "4663": {
                "Class Full Name": "Applied Robotics",
                "Description": "This course provides a solid foundation of robotics including kinematics, programming, safety, common applications, and integration of robotic systems following a System Engineering approach. Concepts are emphasized using a hands-on approach. Students will develop projects and implement solutions to each of the topics discussed in class",
                "Prereqs": {
                    "AND": [
                        {
                            "Department": "EEL",
                            "Course Code": "4657",
                            "Grade": "C"
                        }
                    ]
                },
                "Coreqs": "N/A",
                "Credit Hours": 3
            },
            "4905": {
                "Class Full Name": "Independent Study",
                "Description": "Specialized independent study determined by the students\u2019 needs and interests.",
                "Prereqs": "N/A",
                "Coreqs": "N/A",
                "Credit Hours": 1
            }
        },
        "EGN": {
            "3000": {
                "Class Full Name": "Foundations of Engineering",
                "Description": "Introduction to the USF College of Engineering disciplines and the engineering profession. Course will provide you with knowledge of resources to help you succeed. Course topics include academic policies and procedures, study skills, and career planning.",
                "Prereqs": "N/A",
                "Coreqs": "N/A",
                "Credit Hours": 0
            },
            "3000L": {
                "Class Full Name": "Foundations of Engineering Lab",
                "Description": "Introduction to Engineering and its disciplines incorporating examples of tools and techniques used in design and presentation. Laboratory exercises will include computer tools, engineering design, team projects, and oral and written communication skills.",
                "Prereqs": "N/A",
                "Coreqs": "N/A",
                "Credit Hours": 3
            },
            "3443": {
                "Class Full Name": "Probability and Statistics for Engineers",
                "Description": "An introduction to concepts of probability and statistical analysis with special emphasis on critical interpretation of data, comparing and contrasting claims, critical thinking, problem solving, and writing.",
                "Prereqs": {
                    "OR": [
                        {
                            "Department": "MAC",
                            "Course Code": "2282",
                            "Grade": "C"
                        },
                        {
                            "Department": "MAC",
                            "Course Code": "2312",
                            "Grade": "C"
                        },
                        {
                            "Department": "AP Calculus",
                            "Course Code": "BC",
                            "Grade": "4"
                        }
                    ]
                },
                "Coreqs": "N/A",
                "Credit Hours": 3
            },
            "3615": {
                "Class Full Name": "Engineering Economics with Social and Global Implications",
                "Description": "Presents basic economic models used to evaluate engineering project investments with an understanding of the implications of human and cultural diversity on financial decisions through lectures, problem solving, and critical writing.",
                "Prereqs": "N/A",
                "Coreqs": "N/A",
                "Credit Hours": 3
            },
            "3375": {
                "Class Full Name": "Electromechanical Systems",
                "Description": "Analysis of electromechanical device performance: transformers, transducers, DC motors and generators, AC motors and alternators.",
                "Prereqs": {
                    "AND": [
                        {
                            "Department": "EGN",
                            "Course Code": "3374",
                            "Grade": "C"
                        }
                    ]
                },
                "Coreqs": "N/A",
                "Credit Hours": 3
            },
            "3374": {
                "Class Full Name": "Introduction to Electrical Systems",
                "Description": "A second course in linear passive circuits (following EGN 3373). An extension of the physical principles and models, AC/DC steady-state, transient analysis and power analysis techniques.",
                "Prereqs": {
                    "AND": [
                        {
                            "Department": "EGN",
                            "Course Code": "3373",
                            "Grade": "C"
                        }
                    ]
                },
                "Coreqs": {
                    "OR": [
                        {
                            "Department": "MAP",
                            "Course Code": "2302",
                            "Grade": "C"
                        },
                        {
                            "Department": "EGN",
                            "Course Code": "3433",
                            "Grade": "C"
                        }
                    ]
                },
                "Credit Hours": 3
            }
        },
        "EEE": {
            "3394": {
                "Class Full Name": "Electrical Engineering Science I - Electronic Materials",
                "Description": "This course provides electrical and computer engineering students with a strong background in material science and quantum physics as they relate to electrical/electronic material and device properties and applications.",
                "Prereqs": {
                    "AND": [
                        {
                            "OR": [
                                {
                                    "Department": "CHS",
                                    "Course Code": "2440",
                                    "Grade": "C"
                                },
                                {
                                    "Department": "CMH",
                                    "Course Code": "2045",
                                    "Grade": "C"
                                },
                                {
                                    "Department": "AP",
                                    "Course Code": "Chemistry",
                                    "Grade": "4"
                                }
                            ]
                        },
                        {
                            "OR": [
                                {
                                    "Department": "PHY",
                                    "Course Code": "2048",
                                    "Grade": "C"
                                },
                                {
                                    "Department": "PHY",
                                    "Course Code": "2060",
                                    "Grade": "C"
                                },
                                {
                                    "Department": "AP",
                                    "Course Code": "Physics C: Electricity and Magnetism",
                                    "Grade": "4"
                                }
                            ]
                        }
                    ]
                },
                "Coreqs": {
                    "OR": [
                        {
                            "Department": "MAC",
                            "Course Code": "2283",
                            "Grade": "C"
                        },
                        {
                            "Department": "MAC",
                            "Course Code": "2313",
                            "Grade": "C"
                        }
                    ]
                },
                "Credit Hours": 3
            },
            "4301": {
                "Class Full Name": "Electronics II",
                "Description": "Provides further study in electronic circuits. Includes feedback and frequency response techniques in amplifier design.",
                "Prereqs": {
                    "AND": [
                        {
                            "Department": "EEE",
                            "Course Code": "3302",
                            "Grade": "C"
                        }
                    ]
                },
                "Coreqs": "N/A",
                "Credit Hours": 3
            },
            "4314C": {
                "Class Full Name": "Integrated Circuit Technology",
                "Description": "Physics and Chemistry of integrated circuit and discrete device fabrication, materials limitations, processing schemes, failure and yield analysis. A laboratory is integral to the course.",
                "Prereqs": {
                    "AND": [
                        {
                            "Department": "EEE",
                            "Course Code": "4351C",
                            "Grade": "C"
                        }
                    ]
                },
                "Coreqs": "N/A",
                "Credit Hours": 3
            },
            "4315C": {
                "Class Full Name": "Semiconductor Devices",
                "Description": "An introduction to the fundamentals of semiconductor materials and semiconductor device operation.",
                "Prereqs": {
                    "AND": [
                        {
                            "Department": "EEE",
                            "Course Code": "3394",
                            "Grade": "C"
                        }
                    ]
                },
                "Coreqs": "N/A",
                "Credit Hours": 3
            },
            "4359": {
                "Class Full Name": "Analog CMOS VLSI Design",
                "Description": "This course covers Analog CMOS/VLSI design with topics ranging from devices to circuits and their simulations, and basics of layout design and their simulations.",
                "Prereqs": {
                    "AND": [
                        {
                            "Department": "EEE",
                            "Course Code": "3302",
                            "Grade": "C"
                        }
                    ]
                },
                "Coreqs": {
                    "AND": [
                        {
                            "Department": "EEE",
                            "Course Code": "4301",
                            "Grade": "C"
                        }
                    ]
                },
                "Credit Hours": 3
            },
            "4410": {
                "Class Full Name": "System on a Chip",
                "Description": "This course addresses the newly emerging area of \u201csystem on a chip\u201d, which is envisioned as the next revolution beyond integrated circuits. Students will learn the principles and techniques that are expected to apply to this future technology.",
                "Prereqs": {
                    "AND": [
                        {
                            "Department": "EEE",
                            "Course Code": "3373",
                            "Grade": "N/A"
                        }
                    ]
                },
                "Coreqs": "N/A",
                "Credit Hours": 3
            },
            "4774": {
                "Class Full Name": "Data Analytics",
                "Description": "This course aims to teach the fundamentals of Machine Learning and Statistical Data Analysis. It will cover the related theory in statistical inference and learning, practical Machine Learning algorithms, and several applications in various fields.",
                "Prereqs": {
                    "AND": [
                        {
                            "Department": "EGN",
                            "Course Code": "3443",
                            "Grade": "C"
                        }
                    ]
                },
                "Coreqs": "N/A",
                "Credit Hours": 3
            },
            "4530": {
                "Class Full Name": "Flexible Electronics and Thin-Film Solar Cells",
                "Description": "The course focuses on materials science for designing and characterizing flexible electronics and thin-film solar cells.",
                "Prereqs": {
                    "AND": [
                        {
                            "Department": "EEE",
                            "Course Code": "3394",
                            "Grade": "C"
                        }
                    ]
                },
                "Coreqs": "N/A",
                "Credit Hours": 3
            },
            "4748": {
                "Class Full Name": "Cryptography and Data Security",
                "Description": "This course provides an systematic overview and essential knowledge for engineering students to understand concepts and mechanisms in cryptography and data security in engineering applications.",
                "Prereqs": "N/A",
                "Coreqs": "N/A",
                "Credit Hours": 3
            },
            "4746": {
                "Class Full Name": "Wireless Mobile Computing and Security",
                "Description": "This course provides a systematic view of designing and securing wireless mobile computing systems and networks.",
                "Prereqs": "N/A",
                "Coreqs": "N/A",
                "Credit Hours": 3
            },
            "4506": {
                "Class Full Name": "Biomedical Image Processing",
                "Description": "2D signal processing: image enhancement; edge detection and image segmentation. Medical imaging: 3D computerized tomography, magnetic resonance imaging; single photon emission computed tomography; positron emission tomography; radiographs.",
                "Prereqs": "N/A",
                "Coreqs": "N/A",
                "Credit Hours": 3
            },
            "4423": {
                "Class Full Name": "Quantum Computing and Communications",
                "Description": "While silicon computing is heading toward its quantum limit, new technology frontier of computing and communications to fully take advantage of quantum mechanics by Nobel laureate Dr. R.P. Feynman emerges as one of the most critical technologies for human beings. This course aims at basic knowledge of quantum computing, from qubits, logic gates, algorithms, to quantum computer structure. Due to the integral nature of computing and communications, quantum information, error correcting codes, cryptography, and communications, serves the second part of this course. This course orienting technology toward quantum supremacy is developed suitable for undergraduate seniors.",
                "Prereqs": {
                    "AND": [
                        {
                            "OR": [
                                {
                                    "Department": "EGN",
                                    "Course Code": "2440",
                                    "Grade": "C"
                                },
                                {
                                    "Department": "STA",
                                    "Course Code": "4442",
                                    "Grade": "C"
                                }
                            ]
                        },
                        {
                            "OR": [
                                {
                                    "Department": "EGN",
                                    "Course Code": "3420",
                                    "Grade": "C"
                                },
                                {
                                    "Department": "EGN",
                                    "Course Code": "4450",
                                    "Grade": "C"
                                },
                                {
                                    "Department": "MAS",
                                    "Course Code": "3105",
                                    "Grade": "C"
                                }
                            ]
                        }
                    ]
                },
                "Coreqs": "N/A",
                "Credit Hours": 3
            },
            "4260C": {
                "Class Full Name": "Bioelectricity",
                "Description": "Bioelectricity, generation and transmission from cells through tissues. Electrical activity in and among cells is explored from historical models through hands-on laboratory experience.",
                "Prereqs": "N/A",
                "Coreqs": "N/A",
                "Credit Hours": 3
            },
            "4271": {
                "Class Full Name": "Bioelectronics",
                "Description": "This is the second course in the series covering bioelectrical phenomena and systems. In this course the focus is electronics for biomedical applications, and the objective is to discuss electrical systems pertaining to the human body.",
                "Prereqs": "N/A",
                "Coreqs": "N/A",
                "Credit Hours": 3
            },
            "3414": {
                "Class Full Name": "Fundamentals of Data Structures",
                "Description": "This course introduces essential data structures and algorithms, focusing on real-world applications. Topics include fundamental structures, sorting, stack and queue variants, and memory-efficient formats like sparse and compressed data. Practical exercises help students apply these concepts in program development.",
                "Prereqs": {
                    "AND": [
                        {
                            "Department": "EEE",
                            "Course Code": "2161",
                            "Grade": "C"
                        }
                    ]
                },
                "Coreqs": "N/A",
                "Credit Hours": 4
            },
            "4215": {
                "Class Full Name": "Biomedical Optical Spectroscopy and Imaging",
                "Description": "This course will introduce biomedical optical spectroscopy and imaging, including principles of light-tissue interaction, theoretical & computational modeling of photon diffusion, optical medical device instrumentation, and clinical applications.",
                "Prereqs": "N/A",
                "Coreqs": "N/A",
                "Credit Hours": 3
            },
            "4274": {
                "Class Full Name": "MEMS I: Chemical/Biomedical Sensors and Microfabrication",
                "Description": "The course gives an introduction to MEMS, microfabrication techniques and processes as well as basic design principles of biological and chemical Sensors. The course concentrates on basics of MEMS, different processes involved and principles of sensing.",
                "Prereqs": "N/A",
                "Coreqs": "N/A",
                "Credit Hours": 3
            }
        }
    },
    "Hillsborough CC": {
        "BSC": {
            "1005": {
                "Class Full Name": "BIOLOGICAL FOUNDATIONS",
                "Description": "Biological Foundations course",
                "Credit Hours": 3
            },
            "1005L": {
                "Class Full Name": "BIOLOGICAL FOUNDATIONS LAB",
                "Description": "Biological Foundations Laboratory",
                "Credit Hours": 1
            }
        },
        "ENC": {
            "1101": {
                "Class Full Name": "English Composition I",
                "Description": "English Class",
                "CoReqs": "N/A",
                "Prereqs": "N/A",
                "Credit Hours": 3
            },
            "1102": {
                "Class Full Name": "ENGLISH COMPOSITION II",
                "Description": "English Composition II course",
                "Credit Hours": 3
            }
        }
    }
}
