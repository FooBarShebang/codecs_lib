# Entire Library Requirements and Tests Traceability List

## Relation between modules, classes and the requirements and tests indexing

* entire library - 00x
* module *cobs* - 1xx
* module *vigenere* - 2xx
* module *wichmann_hill* - 3xx
* module *xor_scrambler* - 4xx

## Requirements vs Tests Traceability

| **Requirement ID** | **Covered in test(s)** | **Verified \[YES/NO\]** |
| :----------------- | :--------------------- | :---------------------- |
| REQ-FUN-000        | TEST-A-000             | YES                     |
| REQ-FUN-001        | TEST-A-001             | YES                     |
| REQ-FUN-002        | TEST-A-002             | YES                     |
| REQ-FUN-003        | TEST-A-003             | YES                     |
| REQ-INT-000        | TEST-I-000             | YES                     |
| REQ-IAR-000        | TEST-D-000             | YES                     |
| REQ-IAR-001        | TEST-D-001             | YES                     |
| REQ-IAR-002        | TEST-D-000             | YES                     |
| REQ-UDR-000        | TEST-I-001             | YES                     |
| REQ-FUN-100        | TEST-A-100             | YES                     |
| REQ-FUN-101        | TEST-T-100, TEST-T-101 | YES                     |
| REQ-FUN-110        | TEST-T-100             | YES                     |
| REQ-FUN-120        | TEST-T-101, TEST-T-120 | YES                     |
| REQ-AWM-100        | TEST-T-102             | YES                     |
| REQ-AWM-120        | TEST-T-121             | YES                     |
| REQ-FUN-200        | TEST-A-200             | YES                     |
| REQ-FUN-201        | TEST-A-200             | YES                     |
| REQ-FUN-202        | TEST-T-200             | YES                     |
| REQ-FUN-210        | TEST-T-200, TEST-T-201 | YES                     |
| REQ-FUN-220        | TEST-T-200, TEST-T-201 | YES                     |
| REQ-FUN-230        | TEST-T-201             | YES                     |
| REQ-AWM-200        | TEST-T-202             | YES                     |
| REQ-AWM-201        | TEST-T-203             | YES                     |
| REQ-AWM-202        | TEST-T-204             | YES                     |
| REQ-AWM-210        | TEST-T-210             | YES                     |
| REQ-AWM-220        | TEST-T-220             | YES                     |
| REQ-AWM-230        | TEST-T-230             | YES                     |
| REQ-FUN-300        | TEST-A-300             | YES                     |
| REQ-FUN-301        | TEST-A-300             | YES                     |
| REQ-FUN-302        | TEST-T-300             | YES                     |
| REQ-FUN-310        | TEST-T-310             | YES                     |
| REQ-FUN-320        | TEST-T-320             | YES                     |
| REQ-FUN-321        | TEST-T-321             | YES                     |
| REQ-AWM-300        | TEST-T-311, TEST-T-322 | YES                     |
| REQ-AWM-301        | TEST-T-312, TEST-T-323 | YES                     |
| REQ-AWM-320        | TEST-T-324             | YES                     |
| REQ-FUN-400        | TEST-A-400             | YES                     |
| REQ-FUN-401        | TEST-T-400, TEST-T-401 | YES                     |
| REQ-FUN-410        | TEST-T-400             | YES                     |
| REQ-FUN-420        | TEST-T-401             | YES                     |
| REQ-AWM-400        | TEST-T-402             | YES                     |
| REQ-AWM-401        | TEST-T-403             | YES                     |

| **Software ready for production \[YES/NO\]** | **Rationale**        |
| :------------------------------------------: | :------------------- |
| YES                                          | All tests are passed |
