package org.srvvp.knowledgetree.session;

import org.srvvp.knowledgetree.entity.*;
import org.jboss.seam.annotations.In;
import org.jboss.seam.annotations.Name;
import org.jboss.seam.framework.EntityHome;

@Name("workRelatestoWorkHome")
public class WorkRelatestoWorkHome extends EntityHome<WorkRelatestoWork> {

	@In(create = true)
	WorkHome workHome;
	@In(create = true)
	WorkWorkRelationHome workWorkRelationHome;

	public void setWorkRelatestoWorkId(WorkRelatestoWorkId id) {
		setId(id);
	}

	public WorkRelatestoWorkId getWorkRelatestoWorkId() {
		return (WorkRelatestoWorkId) getId();
	}

	public WorkRelatestoWorkHome() {
		setWorkRelatestoWorkId(new WorkRelatestoWorkId());
	}

	@Override
	public boolean isIdDefined() {
		if (getWorkRelatestoWorkId().getWork1() == null
				|| "".equals(getWorkRelatestoWorkId().getWork1()))
			return false;
		if (getWorkRelatestoWorkId().getWork2() == null
				|| "".equals(getWorkRelatestoWorkId().getWork2()))
			return false;
		return true;
	}

	@Override
	protected WorkRelatestoWork createInstance() {
		WorkRelatestoWork workRelatestoWork = new WorkRelatestoWork();
		workRelatestoWork.setId(new WorkRelatestoWorkId());
		return workRelatestoWork;
	}

	public void load() {
		if (isIdDefined()) {
			wire();
		}
	}

	public void wire() {
		getInstance();
		Work workByWork1 = workHome.getDefinedInstance();
		if (workByWork1 != null) {
			getInstance().setWorkByWork1(workByWork1);
		}
		Work workByWork2 = workHome.getDefinedInstance();
		if (workByWork2 != null) {
			getInstance().setWorkByWork2(workByWork2);
		}
		WorkWorkRelation workWorkRelation = workWorkRelationHome
				.getDefinedInstance();
		if (workWorkRelation != null) {
			getInstance().setWorkWorkRelation(workWorkRelation);
		}
	}

	public boolean isWired() {
		if (getInstance().getWorkByWork1() == null)
			return false;
		if (getInstance().getWorkByWork2() == null)
			return false;
		return true;
	}

	public WorkRelatestoWork getDefinedInstance() {
		return isIdDefined() ? getInstance() : null;
	}

}
