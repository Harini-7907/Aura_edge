import sys
from pathlib import Path

# Add AURA-Edge project root to Python path
PROJECT_ROOT = Path(__file__).resolve().parent.parent

if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))


from orchestration.task_profiler import create_task
from orchestration.resource_profile import create_execution_resources


# ==========================================
# FEASIBILITY CHECK
# ==========================================

def check_feasibility(task, resource):

    reasons = []

    # --------------------------------------
    # Current CPU availability
    # --------------------------------------

    if resource.cpu_available < task.cpu_requirement:

        reasons.append(
            f"Current CPU insufficient "
            f"({resource.cpu_available:.2f}% available)"
        )

    # --------------------------------------
    # Current memory availability
    # --------------------------------------

    if resource.memory_available < task.memory_requirement:

        reasons.append(
            f"Current memory insufficient "
            f"({resource.memory_available:.2f}% available)"
        )

    # --------------------------------------
    # Predicted CPU utilization
    #
    # predicted_cpu is utilization %
    # --------------------------------------

    predicted_cpu_available = (
        100.0 - resource.predicted_cpu
    )

    if predicted_cpu_available < task.cpu_requirement:

        reasons.append(
            f"Predicted CPU insufficient "
            f"({predicted_cpu_available:.2f}% "
            f"available after prediction)"
        )

    # --------------------------------------
    # Predicted memory utilization
    #
    # predicted_memory is utilization %
    # --------------------------------------

    predicted_memory_available = (
        100.0 - resource.predicted_memory
    )

    if predicted_memory_available < task.memory_requirement:

        reasons.append(
            f"Predicted memory insufficient "
            f"({predicted_memory_available:.2f}% "
            f"available after prediction)"
        )

    # --------------------------------------
    # Deadline
    # --------------------------------------

    latency_seconds = resource.latency / 1000.0

    estimated_total_time = (
        latency_seconds
        + task.estimated_execution_time
    )

    if estimated_total_time > task.deadline:

        reasons.append(
            f"Deadline cannot be met "
            f"({estimated_total_time:.3f}s estimated)"
        )

    return reasons


# ==========================================
# SCORE COMPONENTS
# ==========================================

def calculate_score_components(task, resource):

    latency_score = (
        100.0 / (resource.latency + 1.0)
    )

    bandwidth_score = (
        resource.bandwidth / 10.0
    )

    if resource.energy_cost <= 0:

        energy_score = 0.0

    else:

        energy_score = (
            (1.0 / resource.energy_cost) * 10.0
        )

    reliability_score = (
        resource.reliability * 100.0
    )

    # --------------------------------------
    # Risk
    # --------------------------------------

    risk_penalty = 0.0

    if resource.risk == "WARNING":

        risk_penalty = 15.0

    elif resource.risk == "CRITICAL":

        risk_penalty = 40.0

    # --------------------------------------
    # Prediction uncertainty
    # --------------------------------------

    uncertainty_penalty = (
        resource.prediction_uncertainty * 0.5
    )

    # --------------------------------------
    # Future CPU utilization
    # --------------------------------------

    future_cpu_penalty = (
        max(
            0.0,
            resource.predicted_cpu - 70.0
        )
        * 0.5
    )

    # --------------------------------------
    # Future memory utilization
    # --------------------------------------

    future_memory_penalty = (
        max(
            0.0,
            resource.predicted_memory - 70.0
        )
        * 0.5
    )

    # --------------------------------------
    # Task priority
    # --------------------------------------

    priority_penalty = (
        max(
            0,
            task.priority - 1
        )
        * 5.0
    )

    # --------------------------------------
    # Battery
    # --------------------------------------

    battery_penalty = 0.0

    if resource.battery_level < 30:

        battery_penalty = 20.0

    elif resource.battery_level < 50:

        battery_penalty = 10.0

    # --------------------------------------
    # Temperature
    # --------------------------------------

    temperature_penalty = 0.0

    if resource.temperature >= 80:

        temperature_penalty = 25.0

    elif resource.temperature >= 70:

        temperature_penalty = 15.0

    elif resource.temperature >= 60:

        temperature_penalty = 5.0

    # --------------------------------------
    # Final score
    # --------------------------------------

    score = (

        latency_score
        + bandwidth_score
        + energy_score
        + reliability_score

        - risk_penalty
        - uncertainty_penalty
        - future_cpu_penalty
        - future_memory_penalty
        - priority_penalty
        - battery_penalty
        - temperature_penalty
    )

    return {
        "latency_score": latency_score,
        "bandwidth_score": bandwidth_score,
        "energy_score": energy_score,
        "reliability_score": reliability_score,

        "risk_penalty": risk_penalty,
        "uncertainty_penalty": uncertainty_penalty,
        "future_cpu_penalty": future_cpu_penalty,
        "future_memory_penalty": future_memory_penalty,
        "priority_penalty": priority_penalty,
        "battery_penalty": battery_penalty,
        "temperature_penalty": temperature_penalty,

        "final_score": score
    }


# ==========================================
# RESOURCE SCORE
# ==========================================

def calculate_score(task, resource):

    reasons = check_feasibility(
        task,
        resource
    )

    if reasons:

        return None

    components = calculate_score_components(
        task,
        resource
    )

    return components["final_score"]


# ==========================================
# RESOURCE SELECTION
# ==========================================

def select_resource(task, resources):

    results = []

    rejected = []

    for resource in resources:

        reasons = check_feasibility(
            task,
            resource
        )

        if reasons:

            rejected.append(
                (
                    resource,
                    reasons
                )
            )

        else:

            score = calculate_score(
                task,
                resource
            )

            results.append(
                (
                    resource,
                    score
                )
            )

    results.sort(
        key=lambda x: x[1],
        reverse=True
    )

    if results:

        best_resource = results[0][0]

    else:

        best_resource = None

    return (
        best_resource,
        results,
        rejected
    )


# ==========================================
# DECISION EXPLANATION
# ==========================================

def explain_decision(task, resource):

    reasons = check_feasibility(
        task,
        resource
    )

    if reasons:

        return {
            "feasible": False,
            "reasons": reasons,
            "components": None
        }

    components = calculate_score_components(
        task,
        resource
    )

    return {
        "feasible": True,
        "reasons": [],
        "components": components
    }


# ==========================================
# MAIN PROGRAM
# ==========================================

if __name__ == "__main__":

    print(
        "Starting AURA-Edge decision engine..."
    )

    resources = create_execution_resources()

    tasks = [

        # ----------------------------------
        # Latency-sensitive task
        # ----------------------------------

        create_task(
            task_id="latency_task",
            cpu_requirement=40.0,
            memory_requirement=30.0,
            deadline=0.62,
            priority=3,
            estimated_execution_time=0.6,
            task_size=5.0
        ),

        # ----------------------------------
        # CPU-intensive task
        # ----------------------------------

        create_task(
            task_id="compute_task",
            cpu_requirement=85.0,
            memory_requirement=30.0,
            deadline=2.0,
            priority=2,
            estimated_execution_time=1.2,
            task_size=10.0
        ),

        # ----------------------------------
        # Memory-intensive task
        # ----------------------------------

        create_task(
            task_id="memory_task",
            cpu_requirement=40.0,
            memory_requirement=80.0,
            deadline=2.0,
            priority=2,
            estimated_execution_time=1.2,
            task_size=8.0
        )
    ]

    for task in tasks:

        selected, results, rejected = (
            select_resource(
                task,
                resources
            )
        )

        print(
            "\n=========================================="
        )

        print(
            "TASK:",
            task.task_id
        )

        print(
            "=========================================="
        )

        print(
            "CPU requirement:",
            task.cpu_requirement,
            "%"
        )

        print(
            "Memory requirement:",
            task.memory_requirement,
            "%"
        )

        print(
            "Deadline:",
            task.deadline,
            "seconds"
        )

        print(
            "Priority:",
            task.priority
        )

        # ----------------------------------
        # Candidate resources
        # ----------------------------------

        if results:

            print(
                "\nCandidate resources:"
            )

            for resource, score in results:

                print(
                    f"{resource.name}: "
                    f"Score = {score:.2f}"
                )

        # ----------------------------------
        # Rejected resources
        # ----------------------------------

        if rejected:

            print(
                "\nRejected resources:"
            )

            for resource, reasons in rejected:

                print(
                    f"\n{resource.name}:"
                )

                for reason in reasons:

                    print(
                        f"  - {reason}"
                    )

        # ----------------------------------
        # Final selection
        # ----------------------------------

        if selected is None:

            print(
                "\nSelected resource: NONE"
            )

            print(
                "No resource can satisfy the task."
            )

        else:

            print(
                "\nSelected resource:",
                selected.name
            )

            explanation = explain_decision(
                task,
                selected
            )

            components = explanation[
                "components"
            ]

            print(
                "Selected score:",
                f"{components['final_score']:.2f}"
            )

            print(
                "\nDecision explanation:"
            )

            print(
                f"  Latency contribution: "
                f"+{components['latency_score']:.2f}"
            )

            print(
                f"  Bandwidth contribution: "
                f"+{components['bandwidth_score']:.2f}"
            )

            print(
                f"  Energy contribution: "
                f"+{components['energy_score']:.2f}"
            )

            print(
                f"  Reliability contribution: "
                f"+{components['reliability_score']:.2f}"
            )

            print(
                f"  Risk penalty: "
                f"-{components['risk_penalty']:.2f}"
            )

            print(
                f"  Uncertainty penalty: "
                f"-{components['uncertainty_penalty']:.2f}"
            )

            print(
                f"  Future CPU penalty: "
                f"-{components['future_cpu_penalty']:.2f}"
            )

            print(
                f"  Future memory penalty: "
                f"-{components['future_memory_penalty']:.2f}"
            )

            print(
                f"  Battery penalty: "
                f"-{components['battery_penalty']:.2f}"
            )

            print(
                f"  Temperature penalty: "
                f"-{components['temperature_penalty']:.2f}"
            )

    print(
        "\n=========================================="
    )

    print(
        "ALL TASK DECISIONS COMPLETED"
    )

    print(
        "=========================================="
    )