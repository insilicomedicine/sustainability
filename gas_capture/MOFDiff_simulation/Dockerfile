FROM akhmedins/benchmark_raspa2_sim:latest
COPY run_simulation.sh /
RUN chmod +x /run_simulation.sh
SHELL ["/bin/bash", "-c"]
ENTRYPOINT ["/bin/bash", "-c", "source ~/.bashrc && source /root/miniforge3/etc/profile.d/conda.sh && conda activate mofdiff && exec /run_simulation.sh"]