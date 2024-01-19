import streamlit as st

if __name__ == "__main__":
    st.header("How to Use the PC Reservation System")
    st.markdown("## 1. Reserve PC")
    st.markdown("""
                1. Open the "Main" page.
                2. Open the Reservation Form by clicking the "Show Reservation Form" button.
                3. Select your name from the dropdown menu.
                4. Select the PC you want to reserve from the dropdown menu.
                5. Select the start date and time of your reservation.
                6. Select the end date and time of your reservation.
                7. Click the "Reserve" button.
                8. Confirm your reservation by clicking the "Agree" button in the dialog.
                9. If your reservation is successful, you will see a success message.
                """)
    with open("reservation.mp4", "rb") as file:
        video_bytes = file.read()
    st.video(video_bytes)
    st.markdown("## 2. Cancel Reservation")
    st.markdown("""
                1. Open the "Cancel Reservation" page.
                2. Select your name from the dropdown menu.
                3. If you have any reservations, you will see them.
                4. Click the "Cancel Reservation" button.
                5. Confirm your cancellation by clicking the "Agree" button in the dialog.
                6. If your cancellation is successful, you will see a success message.
                """)
    with open("cancel.mp4", "rb") as file:
        video_bytes = file.read()
    st.video(video_bytes)