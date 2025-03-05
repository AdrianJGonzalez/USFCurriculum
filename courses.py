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
            "3113": {
                "Class Full Name": "Intermediate Financial Accounting II",
                "Description": "Continuation of ACG 3103. Topics covered include property, plant and equipment, intangibles, current liabilities, long-term debt, leases, tax allocation, statement of cash flows.",
                "CoReqs": "N/A",
                "Prereqs": [
                    {
                        "Department": "ACG",
                        "Course Code": "3103",
                        "Grade": "C"
                    },
                    [
                        {
                            "Department": "ACG",
                            "Course Code": "3341",
                            "Grade": "C"
                        },
                        {
                            "Department": "ACG",
                            "Course Code": "3401",
                            "Grade": "C"
                        },
                        {
                            "Department": "TAX",
                            "Course Code": "4001",
                            "Grade": "C"
                        }
                    ]
                ],
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
            "3394": {
                "Class Full Name": "Programming with C",
                "Description": "An introductory course to provide the fundamentals of computer language for electrical engineering students. Skills on syntax, functions, data, input and output, algorithm, and creating solutions for engineering problems using C.",
                "Prereqs": "N/A",
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
                            "Grade": "N/A"
                        }
                    ]
                },
                "Coreqs": "N/A",
                "Credit Hours": 1
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
                            "Course Code": "3420",
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
                            "Course Code" = "3420",
                            "Grade": "C"
                        },
                        {
                            "Departnent" : "EGN"
                            "Course Code" : "3374"
                            "Grade" : "B"
                        }
                    ]
                },
                "Coreqs": "N/A",
                "Credit Hours": 3
            },
            "3115L" : {
                "Class Full Name": "Laboratory I",
                "Description": "Basic circuit theory applications; computer-aided design tools, electrical measurement techniques.",
                "Prereqs": {
                    "AND": [
                        {
                            "Department" : "EGN",
                            "Course Code" = "3373",
                            "Grade" = "C"
                        }
                    ]
                },
                "Coreqs": "N/A",
                "Credit Hours": 1
            },
            "3116L" : {
                "Class Full Name": "Laboratory II",
                "Description": "This larboratory is designed to introduce electrical engineering students to the design, building and testing of active electronic networks. Computer Aided Design tools and computer data acquistition strategies are examined in greater detail.",
                "Prereqs": {
                    "AND": [
                        {
                            "Department" : "EEE",
                            "Course Code" : "3302",
                            "Grade" : "C"
                        },
                        {
                            "Department" : "EEL"
                            "Course Code" : "EEL"
                            "Grade" : "3115L"
                        }
                    ]
                },
                "Coreqs": "N/A",
                "Credit Hours": 1
            },
            "3472C": {
                "Class Full Name": "Electrical Engineering Science II - Electromagnetics",
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
                "Credit Hours": 3
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
                        },
                    ]
                },
                "Coreqs": {
                    "AND": [
                        {
                            "Department": "EGN",
                            "Course Code": "3375",
                            "Grade": "C"
                        },
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
                        },
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
                "Coreqs": "N/A"
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
                "Coreqs": "N/A"
                "Credit Hours": 3
            },
            "4251": {
                "Class Full Name": "Power System Analysis",
                "Description": "This course will introduce analysis and opertation of power systems. The topics covered in this course nclude per unit sysetm, load flow analysis, voltage stability, economic dispatch, state estimation and power system economics.",
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
                "Coreqs":"N/A",
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
                        },
                    ]
                },
                "Coreqs":"N/A",
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
                        },
                    ]
                },
                "Coreqs":"N/A",
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
                        },
                        
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
                "Coreqs":"N/A",
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
                        },
                    ]
                },
                "Coreqs": "N/A",
                "Credit Hours": 3
            },
            "4102": {
                "Class Full Name": "Wireless Commiunication Systems Laboratory",
                "Description": "The course provides an extensive hands-on introduction to digital and wireless communication systems; involving testing, modeling, simulation, and measurements of the performance of digital communication systems at both sub-system and system levels. Wireless channel and its effect on the system will be reviewed. Ways to counteract the channel and radio impairments will be practically shown.",
                "Prereqs": {
                    "AND": [
                        {
                            "Department": "EEL",
                            "Course Code": "4512C",
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
            "4540": {
                "Class Full Name": "Radar Systems",
                "Description": "The course provides a comprehensive introduction to radar systems and applications. The course examines radar concepts at both the systems and the syb-system level. Electromagnetic propagation, scattering, and antenna concepts are discussed. Wireless system design, signal processing, and radar imaging topics are analyzed.",
                "Prereqs": {
                    "AND": [
                        {
                            "Department": "EEL",
                            "Course Code": "4423C",
                            "Grade": "C"
                        },
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
                        },{
                            "AND": [
                                {
                                    "Department" : "PHY",
                                    "Course Code":"2049",
                                    "Grade":"C"
                                },
                                {
                                    "Department":"PHY",
                                    "Course Code":"2049L",
                                    "Grade":"C"
                                }
                            ]
                        }
                    ]
                },
                "Coreqs": "N/A",
                "Credit Hours": 3
            },
            "4657L": {
                "Class Full Name": "Linear Contol Systems Laboratory",
                "Description": "This laboratory introduces students to the techniques needed for the design and implementation of automatic industrial control systems. Students will learn the basics of the software and hardware used for the design and implementation of control systems.",
                "Prereqs": "N/A",
                "Coreqs": {
                    "AND": [
                        {
                            "Department": "EEL",
                            "Course Code": "4657",
                            "Grade": "C"
                        },
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
                        },

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
                        },
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
                        },
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
                        },
                    ]
                },
                "Coreqs": "N/A",
                "Credit Hours": 3
            },
            "4782": {
                "Class Full Name": "Data Networks and Systems and Security",
                "Description": "The objective of thsi course is to provide a technical and operational introduction to data/computer communication networks, including network management and security.",
                "Prereqs": {
                    "AND": [
                        {
                            "Department": "EGEELN",
                            "Course Code": "2161",
                            "Grade": "C"
                        },
                    ]
                },
                "Coreqs":"N/A",
                "Credit Hours": 3
            },
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
            }
        }
    },
    "Hillsborough CC": {
        "ENC": {
            "1101": {
                "Class Full Name": "English Composition I",
                "Description": "English Class",
                "CoReqs": "N/A",
                "Prereqs": "N/A",
                "Credit Hours": 3
            }
        }
    }
}
