# ==========================================
# AURA-Edge Prediction Uncertainty
# ==========================================

RESOURCE_UNCERTAINTY = {
    "target_cpu": 7.7837,
    "target_memory": 1.9066,
    "target_net_in": 0.0106,
    "target_net_out": 0.0092,
    "target_disk": 4.6713
}


def get_resource_uncertainty():

    return RESOURCE_UNCERTAINTY.copy()


if __name__ == "__main__":

    print("==========================================")
    print("AURA-Edge PREDICTION UNCERTAINTY")
    print("==========================================")

    uncertainty = get_resource_uncertainty()

    for resource, value in uncertainty.items():

        print(
            f"{resource}: "
            f"{value:.4f}"
        )

    print("==========================================")
    print("UNCERTAINTY CONFIGURATION LOADED")
    print("==========================================")
    