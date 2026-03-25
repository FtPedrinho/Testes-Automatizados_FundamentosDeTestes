import pytest
from scholarship_system import evaluate_scholarship, Status

# --- TESTES FUNCIONAIS (REQUISITOS) ---

def test_approved_case():
    """Caso de APPROVED: Atende a todos os requisitos mínimos."""
    result = evaluate_scholarship(18, 8.5, 92.0, True, False)
    assert result.status == Status.APPROVED

def test_manual_review_case():
    """Caso de MANUAL_REVIEW: Idade entre 16 e 17."""
    result = evaluate_scholarship(17, 8.5, 92.0, True, False)
    assert result.status == Status.MANUAL_REVIEW

@pytest.mark.parametrize("age, gpa, att, courses, disc, reason", [
    (15, 8.5, 92.0, True, False, "younger than the minimum"), # Idade < 16
    (19, 5.0, 92.0, True, False, "GPA is below"),              # GPA < 6.0
    (19, 8.5, 70.0, True, False, "Attendance rate is below"),  # Frequência < 75%
])
def test_rejected_reasons(age, gpa, att, courses, disc, reason):
    """3 Casos de REJECTED por motivos diferentes."""
    result = evaluate_scholarship(age, gpa, att, courses, disc)
    assert result.status == Status.REJECTED
    assert any(reason in r for r in result.reasons)

# --- TESTES DE VALOR LIMITE (FRONTEIRAS) ---

@pytest.mark.parametrize("gpa, expected_status", [
    (5.9, Status.REJECTED),      # Limite inferior de erro
    (6.0, Status.MANUAL_REVIEW), # Exatamente o limite de Review
    (6.9, Status.MANUAL_REVIEW), # Limite superior de Review
    (7.0, Status.APPROVED),      # Exatamente o limite de Aprovação
])
def test_gpa_boundaries(gpa, expected_status):
    result = evaluate_scholarship(19, gpa, 90.0, True, False)
    assert result.status == expected_status

# --- ENTRADAS INVÁLIDAS ---

def test_invalid_gpa():
    with pytest.raises(ValueError, match="GPA must be between 0 and 10"):
        evaluate_scholarship(20, 11.0, 90.0, True, False)