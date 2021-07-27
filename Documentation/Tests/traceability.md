# Entire Library Requirements and Tests Traceability List

## Relation between modules, classes and the requirements and tests indexing

* entire library - 00x
* module *cobs* - 1xx
* module *vigenere* - 2xx
* module *xor_scrambler* - 4xx

## Requirements vs Tests Traceability

| **Requirement ID** | **Covered in test(s)** | **Verified \[YES/NO\]**) |
| :----------------- | :--------------------- | :----------------------- |
| REQ-FUN-000        | TEST-A-000             | YES                      |
| REQ-FUN-001        | TEST-A-001             | YES                      |
| REQ-FUN-002        | TEST-A-002             | NO                       |
| REQ-FUN-003        | TEST-A-003             | YES                      |
| REQ-INT-000        | TEST-I-000             | NO                       |
| REQ-IAR-000        | TEST-D-000             | NO                       |
| REQ-IAR-001        | TEST-D-001             | NO                       |
| REQ-IAR-002        | TEST-D-000             | NO                       |
| REQ-UDR-000        | TEST-I-001             | NO                       |
| REQ-FUN-100        | TEST-A-100             | YES                      |
| REQ-FUN-101        | TEST-T-100, TEST-T-101 | YES                      |
| REQ-FUN-110        | TEST-T-100             | YES                      |
| REQ-FUN-120        | TEST-T-101, TEST-T-120 | YES                      |
| REQ-AWM-100        | TEST-T-102             | YES                      |
| REQ-AWM-120        | TEST-T-121             | YES                      |
| REQ-FUN-200        | TEST-A-200             | YES                      |
| REQ-FUN-201        | TEST-A-200             | YES                      |
| REQ-FUN-202        | TEST-T-200             | YES                      |
| REQ-FUN-210        | TEST-T-200, TEST-T-201 | YES                      |
| REQ-FUN-220        | TEST-T-200, TEST-T-201 | YES                      |
| REQ-FUN-230        | TEST-T-201             | YES                      |
| REQ-AWM-200        | TEST-T-202             | YES                      |
| REQ-AWM-201        | TEST-T-203             | YES                      |
| REQ-AWM-202        | TEST-T-204             | YES                      |
| REQ-AWM-210        | TEST-T-210             | YES                      |
| REQ-AWM-220        | TEST-T-220             | YES                      |
| REQ-AWM-230        | TEST-T-230             | YES                      |
| REQ-FUN-400        | TEST-A-400             | YES                      |
| REQ-FUN-401        | TEST-T-400, TEST-T-401 | YES                      |
| REQ-FUN-410        | TEST-T-400             | YES                      |
| REQ-FUN-420        | TEST-T-401             | YES                      |
| REQ-AWM-400        | TEST-T-402             | YES                      |
| REQ-AWM-401        | TEST-T-403             | YES                      |

| **Software ready for production \[YES/NO\]** | **Rationale**        |
| :------------------------------------------: | :------------------- |
| NO                                           | Under development    |
