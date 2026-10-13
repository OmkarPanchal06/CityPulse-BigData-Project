FROM eclipse-temurin:8-jdk-jammy
ARG DEBIAN_FRONTEND=noninteractive
ARG HADOOP_VERSION=3.3.6
ARG HIVE_VERSION=3.1.3
ENV HADOOP_HOME=/opt/hadoop
ENV HIVE_HOME=/opt/hive
ENV PATH=${HADOOP_HOME}/bin:${HADOOP_HOME}/sbin:${HIVE_HOME}/bin:${PATH}
RUN apt-get update && apt-get install -y --no-install-recommends \
    python3 python3-pip python3-venv curl wget procps netcat-openbsd \
    build-essential git ca-certificates bash tini && \
    rm -rf /var/lib/apt/lists/*
RUN curl -fL "https://archive.apache.org/dist/hadoop/common/hadoop-${HADOOP_VERSION}/hadoop-${HADOOP_VERSION}.tar.gz" -o /tmp/hadoop.tgz && \
    tar -xzf /tmp/hadoop.tgz -C /opt && mv "/opt/hadoop-${HADOOP_VERSION}" "$HADOOP_HOME" && rm /tmp/hadoop.tgz
RUN curl -fL "https://archive.apache.org/dist/hive/hive-${HIVE_VERSION}/apache-hive-${HIVE_VERSION}-bin.tar.gz" -o /tmp/hive.tgz && \
    tar -xzf /tmp/hive.tgz -C /opt && mv "/opt/apache-hive-${HIVE_VERSION}-bin" "$HIVE_HOME" && rm /tmp/hive.tgz
# Hive 3.1.3 bundles an older Guava; use Hadoop's Guava consistently on the classpath.
RUN HGUAVA=$(find "$HADOOP_HOME/share/hadoop/common/lib" -maxdepth 1 -name 'guava-*.jar' | head -1) && \
    test -n "$HGUAVA" && rm -f "$HIVE_HOME/lib/guava-*.jar" && cp "$HGUAVA" "$HIVE_HOME/lib/"
RUN mkdir -p /workspace /opt/hadoop-data /opt/hive-warehouse && \
    echo 'export JAVA_HOME=/opt/java/openjdk' >> "$HADOOP_HOME/etc/hadoop/hadoop-env.sh" && \
    echo 'export HADOOP_OPTS="-Djava.library.path=${HADOOP_HOME}/lib/native"' >> "$HADOOP_HOME/etc/hadoop/hadoop-env.sh"
WORKDIR /workspaces/CityPulse-BigData-Project
COPY requirements.txt /tmp/requirements.txt
RUN python3 -m pip install --no-cache-dir -r /tmp/requirements.txt
ENV HIVE_CONF_DIR=${HIVE_HOME}/conf
RUN printf '%s\n' \
 '<configuration>' \
 ' <property><name>javax.jdo.option.ConnectionURL</name><value>jdbc:derby:;databaseName=/opt/hive-metastore/metastore_db;create=true</value></property>' \
 ' <property><name>hive.metastore.schema.verification</name><value>false</value></property>' \
 ' <property><name>datanucleus.schema.autoCreateAll</name><value>true</value></property>' \
 ' <property><name>hive.exec.scratchdir</name><value>/tmp/hive-scratch</value></property>' \
 ' <property><name>hive.exec.local.scratchdir</name><value>/tmp/hive-local</value></property>' \
 ' <property><name>hive.metastore.warehouse.dir</name><value>file:///opt/hive-warehouse</value></property>' \
 '</configuration>' > "$HIVE_HOME/conf/hive-site.xml" && mkdir -p /opt/hive-metastore
